#!/usr/bin/env node
/**
 * Pull a Google Sheet tab via the Sheets API (read-only) and write
 * src/data/audit-sheet-rows.json — same shape as the CSV importer.
 *
 * **Why use this:** API grid data preserves links. CSV export often drops them.
 * - Single-link cells may set `hyperlink`.
 * - **Multi-link rich text** leaves `hyperlink` empty; URLs are only in
 *   `textFormatRuns[].format.link.uri` — this script merges those into `[label](url)` text.
 *
 * Setup:
 *   1. In Google Cloud Console: enable "Google Sheets API", create a service account, download JSON key.
 *   2. Share the spreadsheet with the service account email (Editor not required; Viewer is enough).
 *   3. Save the key file outside the repo or point env at it:
 *        export GOOGLE_APPLICATION_CREDENTIALS="$PWD/.secrets/google-sheets-sa.json"
 *
 * Env (optional defaults for your AU2 prep sheet):
 *   GOOGLE_APPLICATION_CREDENTIALS — path to service account JSON (required)
 *   AUDIT_SHEET_SPREADSHEET_ID — default: 18cdxReyj4i8AecXh5WxKrZ_XyBCgBwjyWLiSpikURuE
 *   AUDIT_SHEET_GID — tab id from URL &gid=… — default: 1746303696
 *
 * Usage:
 *   npm run import-audit-sheet-google
 *   node scripts/import-audit-sheet-google.mjs [spreadsheetId] [gid]
 */

import { google } from "googleapis";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import {
  buildPayloadFromRecords,
  richTextRunsToMarkdownWithLinks,
} from "./sheet-import-pipeline.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, "..");
const outPath = path.join(root, "src", "data", "audit-sheet-rows.json");

const DEFAULT_SPREADSHEET_ID =
  "18cdxReyj4i8AecXh5WxKrZ_XyBCgBwjyWLiSpikURuE";
const DEFAULT_GID = "1746303696";

function a1Escape(title) {
  return `'${String(title).replace(/'/g, "''")}'`;
}

/**
 * Raw cell string before normalizeCellValue (HYPERLINK expansion, etc.).
 * @param {{ richTextCellsWithLinks?: number }} [stats]
 */
function gridCellToRawString(cell, stats) {
  if (!cell) return "";
  const formula = cell.userEnteredValue?.formulaValue;
  if (formula && /^=HYPERLINK\s*\(/i.test(String(formula).trim())) {
    return String(formula).trim();
  }
  const display =
    cell.formattedValue != null && cell.formattedValue !== ""
      ? String(cell.formattedValue)
      : cell.effectiveValue?.stringValue != null
        ? String(cell.effectiveValue.stringValue)
        : cell.effectiveValue?.numberValue != null
          ? String(cell.effectiveValue.numberValue)
          : cell.effectiveValue?.boolValue != null
            ? String(cell.effectiveValue.boolValue)
            : "";

  /**
   * Run startIndex is in UTF-16 code units of the user-entered string when the
   * cell is literal text (see CellData.textFormatRuns). formattedValue can differ
   * (display format), which would desync slices from links.
   */
  const entered =
    cell.userEnteredValue?.stringValue != null
      ? String(cell.userEnteredValue.stringValue)
      : "";
  const displayForRuns = entered.length > 0 ? entered : display;

  const runs = cell.textFormatRuns;
  if (Array.isArray(runs) && runs.length > 0) {
    const merged = richTextRunsToMarkdownWithLinks(displayForRuns, runs);
    if (merged != null) {
      if (
        stats &&
        runs.some((r) => r.format?.link?.uri)
      ) {
        stats.richTextCellsWithLinks =
          (stats.richTextCellsWithLinks ?? 0) + 1;
      }
      return merged.trim();
    }
  }

  const link = cell.hyperlink;
  if (link) {
    const d = display.trim();
    const u = String(link).trim();
    if (d && d !== u) return `${d}\n${u}`;
    return u;
  }
  if (formula && String(formula).trim()) {
    return String(formula).trim();
  }
  return display.trim();
}

async function resolveSheetTitle(sheets, spreadsheetId, gid) {
  const meta = await sheets.spreadsheets.get({
    spreadsheetId,
    fields: "sheets.properties",
  });
  const list = meta.data.sheets || [];
  if (gid != null && String(gid).trim() !== "") {
    const id = Number(gid);
    const found = list.find((s) => s.properties.sheetId === id);
    if (found) return found.properties.title;
    console.warn(
      `  Warning: no tab with sheetId=${id}; using first sheet "${list[0]?.properties?.title}".`,
    );
  }
  if (list[0]?.properties?.title) return list[0].properties.title;
  throw new Error("Spreadsheet has no sheets.");
}

function gridToRecords(rowData, stats) {
  if (!rowData?.length) return [];

  const headerRow = rowData[0];
  const headers = (headerRow?.values || []).map((c, j) =>
    gridCellToRawString(c, stats) || `Column_${j + 1}`,
  );

  const records = [];
  for (let i = 1; i < rowData.length; i++) {
    const row = rowData[i];
    const cells = row?.values || [];
    const obj = {};
    let any = false;
    for (let j = 0; j < headers.length; j++) {
      const key = headers[j];
      const val = gridCellToRawString(cells[j], stats);
      if (val) any = true;
      obj[key] = val;
    }
    if (any) records.push(obj);
  }
  return records;
}

async function main() {
  const keyPath = process.env.GOOGLE_APPLICATION_CREDENTIALS;
  if (!keyPath || !fs.existsSync(path.resolve(keyPath))) {
    console.error(
      "Set GOOGLE_APPLICATION_CREDENTIALS to a service account JSON key file path.\n" +
        "Example: export GOOGLE_APPLICATION_CREDENTIALS=\"$PWD/.secrets/google-sheets-sa.json\"\n" +
        "Share the spreadsheet with the service account email (Viewer is enough).",
    );
    process.exit(1);
  }

  const spreadsheetId =
    process.argv[2] ||
    process.env.AUDIT_SHEET_SPREADSHEET_ID ||
    DEFAULT_SPREADSHEET_ID;
  const gid = process.argv[3] ?? process.env.AUDIT_SHEET_GID ?? DEFAULT_GID;

  const auth = new google.auth.GoogleAuth({
    keyFile: path.resolve(keyPath),
    scopes: ["https://www.googleapis.com/auth/spreadsheets.readonly"],
  });
  const authClient = await auth.getClient();
  const sheets = google.sheets({ version: "v4", auth: authClient });

  const title = await resolveSheetTitle(sheets, spreadsheetId, gid);
  const range = `${a1Escape(title)}!A1:ZZ3000`;

  console.log(`  Spreadsheet: ${spreadsheetId}`);
  console.log(`  Tab: "${title}" (gid=${gid})`);
  console.log(`  Range: ${range}`);

  const res = await sheets.spreadsheets.get({
    spreadsheetId,
    ranges: [range],
    includeGridData: true,
  });

  const sheetBlock = res.data.sheets?.[0];
  const grid = sheetBlock?.data?.[0];
  const rowData = grid?.rowData;
  if (!rowData?.length) {
    console.error("No grid data returned (empty tab or range).");
    process.exit(1);
  }

  const stats = { richTextCellsWithLinks: 0 };
  const rawRecords = gridToRecords(rowData, stats);

  const { payload, hyperlinkFormulasExpanded, excluded } = buildPayloadFromRecords(
    rawRecords,
    `Generated by scripts/import-audit-sheet-google.mjs from spreadsheet ${spreadsheetId} tab "${title}" (gid ${gid}).`,
  );

  fs.writeFileSync(outPath, JSON.stringify(payload, null, 2) + "\n", "utf8");
  console.log(
    `\nWrote ${outPath}\n  Rows: ${payload.rows.length}, columns kept: ${payload.columns.length}`,
  );
  if (hyperlinkFormulasExpanded > 0) {
    console.log(
      `  HYPERLINK formulas expanded: ${hyperlinkFormulasExpanded} cell(s).`,
    );
  }
  if (stats.richTextCellsWithLinks > 0) {
    console.log(
      `  Rich text (textFormatRuns) cells with links: ${stats.richTextCellsWithLinks}.`,
    );
  }
  console.log("  Excluded headers:", excluded.join("; ") || "(none)");
}

main().catch((err) => {
  console.error(err.message || err);
  process.exit(1);
});
