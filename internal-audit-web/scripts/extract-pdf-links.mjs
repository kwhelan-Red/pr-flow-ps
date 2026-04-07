#!/usr/bin/env node
/**
 * Extract hyperlink targets from a PDF (AU2 master template, etc.).
 *
 * 1) Uses pdfjs link annotations when present (parsesHyperlinks → [label](url) in text).
 * 2) Falls back to regex on raw text for plain-text URLs (often truncated in PDFs).
 *
 * For a complete, non-truncated import, prefer the spreadsheet CSV / Google import:
 *   npm run import-audit-sheet -- "~/Downloads/...Master.csv"
 *
 * Usage:
 *   node scripts/extract-pdf-links.mjs [path-to.pdf]
 *   npm run extract-pdf-links -- "~/Downloads/....pdf"
 *
 * Writes: src/data/audit-pdf-links.json (list of unique URLs + markdown links found)
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { PDFParse } from "pdf-parse";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, "..");
const defaultPdf = path.join(
  process.env.HOME || "",
  "Downloads",
  "AU2 Secure Flow + SSC - Simplified Questions - Internal Audit Prep - Template - Master.pdf",
);
const outPath = path.join(root, "src", "data", "audit-pdf-links.json");

const pdfPath = path.resolve(process.argv[2] || defaultPdf);

if (!fs.existsSync(pdfPath)) {
  console.error("PDF not found:", pdfPath);
  console.error(
    "Pass the full path: npm run extract-pdf-links -- /path/to/Master.pdf",
  );
  process.exit(1);
}

const buf = fs.readFileSync(pdfPath);
const parser = new PDFParse({ data: new Uint8Array(buf) });

const plain = await parser.getText({ parseHyperlinks: false });
const withLinks = await parser.getText({ parseHyperlinks: true });
await parser.destroy();

const mdLinks = [...withLinks.text.matchAll(/\[([^\]]+)]\((https?:\/\/[^)]+)\)/g)].map(
  (m) => ({ label: m[1], url: m[2] }),
);

const urlRegex = /https?:\/\/[^\s\]\)>"'\\]+/g;
const fromPlain = [...plain.text.matchAll(urlRegex)].map((m) => m[0]);
const fromMd = mdLinks.map((x) => x.url);
const allRaw = [...fromMd, ...fromPlain];

function tidy(u) {
  return u.replace(/[)\].,;'"]+$/g, "").trim();
}

const unique = [];
const seen = new Set();
for (const u of allRaw.map(tidy)) {
  if (!u || u.length < 12) continue;
  if (seen.has(u)) continue;
  seen.add(u);
  unique.push(u);
}

/** Heuristic: PDF line breaks often chop URLs */
function looksTruncated(u) {
  if (/https?:\/\/[a-z0-9.-]+$/i.test(u)) return true;
  if (u.endsWith("-") || u.endsWith("_")) return true;
  if (/\?$/u.test(u) && u.length < 40) return true;
  return false;
}

const payload = {
  generatedAt: new Date().toISOString(),
  sourcePdf: pdfPath,
  note:
    "PDFs often lack link annotations; URLs may be truncated. Use Master.csv or import-audit-sheet-google for authoritative text.",
  annotationMarkdownLinksFound: mdLinks.length,
  uniqueUrls: unique.length,
  urlsTruncationWarnings: unique.filter(looksTruncated),
  urls: unique,
  markdownLinks: mdLinks,
};

fs.writeFileSync(outPath, JSON.stringify(payload, null, 2) + "\n", "utf8");
console.log(`Wrote ${outPath}`);
console.log(`  Unique URLs (regex + annotations): ${unique.length}`);
console.log(`  [text](url) from PDF links: ${mdLinks.length}`);
console.log(
  `  Flagged possibly truncated: ${payload.urlsTruncationWarnings.length}`,
);
