import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/**
 * Expand Google Sheets HYPERLINK formulas so URLs survive into JSON.
 */
export function expandSheetsHyperlinkFormula(s) {
  const t = String(s).trim();
  const m2 = t.match(
    /^=HYPERLINK\s*\(\s*"([^"]+)"\s*[,;]\s*"([^"]*)"\s*\)\s*$/i,
  );
  if (m2) {
    const url = m2[1].trim();
    const label = (m2[2] ?? "").trim();
    if (label && label !== url) return `${label}\n${url}`;
    return url;
  }
  const m1 = t.match(/^=HYPERLINK\s*\(\s*"([^"]+)"\s*\)\s*$/i);
  if (m1) return m1[1].trim();
  return t;
}

export function normalizeCellValue(v) {
  if (v == null || v === "") return "";
  const s = String(v).trim();
  if (!s) return "";
  if (/^=HYPERLINK\s*\(/i.test(s)) return expandSheetsHyperlinkFormula(s);
  return s;
}

/**
 * Google Sheets: if a cell has multiple Insert→Link ranges, `hyperlink` is empty
 * and URLs only appear in `textFormatRuns[].format.link.uri` (see CellData docs).
 * Rebuild as markdown [label](url) so importers and LinkifiedText keep one link per span.
 *
 * @param {string} display `formattedValue` (same string the run indices refer to; UTF-16)
 * @param {Array<{ startIndex?: number, format?: { link?: { uri?: string } } }>} runs
 * @returns {string|null} merged string, or null if `runs` is not usable
 */
export function richTextRunsToMarkdownWithLinks(display, runs) {
  if (!Array.isArray(runs) || runs.length === 0) return null;
  const text = display == null ? "" : String(display);
  const clamp = (n) =>
    Math.max(0, Math.min(Number(n) || 0, text.length));
  const sorted = [...runs].sort(
    (a, b) => (a.startIndex ?? 0) - (b.startIndex ?? 0),
  );
  let out = "";
  let cursor = 0;
  for (let i = 0; i < sorted.length; i++) {
    const start = clamp(sorted[i].startIndex ?? 0);
    if (start > cursor) {
      out += text.slice(cursor, start);
    }
    const end = clamp(
      i + 1 < sorted.length
        ? (sorted[i + 1].startIndex ?? text.length)
        : text.length,
    );
    const segment = text.slice(start, end);
    const uri = sorted[i].format?.link?.uri;
    if (uri && segment) {
      const label = segment.replace(/\]/g, "›");
      out += `[${label}](${uri})`;
    } else {
      out += segment;
    }
    cursor = end;
  }
  if (cursor < text.length) {
    out += text.slice(cursor);
  }
  return out;
}

export function normalizeRow(rec) {
  const out = {};
  for (const [k, v] of Object.entries(rec)) {
    const key = String(k).trim();
    if (!key) continue;
    out[key] = normalizeCellValue(v);
  }
  return out;
}

function loadConfig(configPath) {
  let config = { excludeColumnsExact: [], excludeColumnSubstrings: [] };
  try {
    config = JSON.parse(fs.readFileSync(configPath, "utf8"));
  } catch {
    /* use defaults */
  }
  return config;
}

function excludeColumn(header, exact, subs) {
  const h = header.trim();
  const lower = h.toLowerCase();
  if (exact.has(lower)) return true;
  for (const sub of subs) {
    if (!sub) continue;
    if (lower.includes(sub)) return true;
  }
  return false;
}

/**
 * @param {Record<string, string>[]} records Raw row objects (strings; may include =HYPERLINK formulas)
 * @param {string} sourceNote
 * @param {{ configPath?: string }} [opts]
 */
export function buildPayloadFromRecords(records, sourceNote, opts = {}) {
  const configPath =
    opts.configPath ?? path.join(__dirname, "sheet-import.config.json");

  let hyperlinkFormulasExpanded = 0;
  for (const rec of records) {
    for (const v of Object.values(rec)) {
      if (v != null && /^=HYPERLINK\s*\(/i.test(String(v).trim())) {
        hyperlinkFormulasExpanded++;
      }
    }
  }

  const rows = records.map((r) => normalizeRow(r));
  const allKeys = new Set();
  for (const row of rows) {
    for (const k of Object.keys(row)) {
      allKeys.add(k);
    }
  }

  const config = loadConfig(configPath);
  const exact = new Set(
    (config.excludeColumnsExact ?? []).map((s) => String(s).trim().toLowerCase()),
  );
  const subs = (config.excludeColumnSubstrings ?? []).map((s) =>
    String(s).trim().toLowerCase(),
  );

  const columns = [];
  const seen = new Set();
  function pushCol(c) {
    const k = c.trim();
    if (!k || excludeColumn(k, exact, subs) || seen.has(k)) return;
    seen.add(k);
    columns.push(k);
  }
  for (const row of rows) {
    for (const k of Object.keys(row)) {
      pushCol(k);
    }
  }

  const trimmedRows = rows.map((row) => {
    const next = {};
    for (const col of columns) {
      next[col] = row[col] ?? "";
    }
    return next;
  });

  const payload = {
    generatedAt: new Date().toISOString(),
    sourceNote,
    columns,
    rows: trimmedRows,
  };

  const excluded = [...allKeys].filter((c) => !columns.includes(c));

  return {
    payload,
    hyperlinkFormulasExpanded,
    excluded,
    columns,
    trimmedRows,
  };
}
