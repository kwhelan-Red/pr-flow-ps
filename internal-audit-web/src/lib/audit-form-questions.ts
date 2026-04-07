import auditSheet from "@/data/audit-sheet-rows.json";
import { auditQuestions } from "@/data";
import type { AuditFormQuestion } from "@/types/audit-form";

/** Column headers from "AU2 Secure Flow + SSC" internal audit prep template CSV. */
const COL_NUM = "#";
const COL_CONTROL = "Category (Control)";
const COL_SOC2 = "SOC2 CCs (Category Example 1)";
const COL_ENG = "Category (Engineering)";
const COL_QUESTION = "Questions/Evidence Requirements";
const COL_HINT = "Hints/Guidance";
const COL_DOCS = "Supported Documents - Good to Have for Readiness";
const COL_BU_RESPONSE = "BU Response";
const COL_BU_ANSWER = "BU Answer";
const COL_BU_EVIDENCE = "BU Supporting Evidence";

const DEFAULT_OPTIONS = ["Yes", "No", "Not Sure", "Not Applicable"] as const;

function rowText(row: Record<string, string>, header: string): string {
  if (row[header] != null && String(row[header]).trim() !== "") {
    return String(row[header]).trim();
  }
  const key = Object.keys(row).find(
    (k) => k.trim().toLowerCase() === header.trim().toLowerCase(),
  );
  if (key && row[key] != null) return String(row[key]).trim();
  return "";
}

type SheetPayload = {
  rows: Record<string, string>[];
};

function buildCategory(row: Record<string, string>): string {
  const control = (row[COL_CONTROL] ?? "").trim();
  const eng = (row[COL_ENG] ?? "").trim();
  if (control && eng) return `${control} · ${eng}`;
  return control || eng || "Question";
}

function isTemplateSheet(rows: Record<string, string>[]): boolean {
  if (!rows.length) return false;
  const keys = new Set(Object.keys(rows[0]));
  return keys.has(COL_QUESTION) && keys.has(COL_HINT);
}

/**
 * Questions loaded from imported Google Sheet (one row = one control).
 * Empty when JSON is empty or not the expected template shape.
 */
export function getSheetTemplateQuestions(): AuditFormQuestion[] {
  const { rows } = auditSheet as SheetPayload;
  if (!isTemplateSheet(rows)) return [];

  const out: AuditFormQuestion[] = [];
  for (let i = 0; i < rows.length; i++) {
    const row = rows[i];
    const question = (row[COL_QUESTION] ?? "").trim();
    if (!question) continue;

    const num = (row[COL_NUM] ?? "").trim();
    const id = num || String(i + 1);

    const soc2 = (row[COL_SOC2] ?? "").trim();
    const hint = (row[COL_HINT] ?? "").trim();
    const docs = (row[COL_DOCS] ?? "").trim();
    const buResponse = rowText(row, COL_BU_RESPONSE);
    const buAnswer = rowText(row, COL_BU_ANSWER);
    const buEvidence = rowText(row, COL_BU_EVIDENCE);

    out.push({
      id,
      category: buildCategory(row),
      question,
      hint,
      supportedDocs: docs || undefined,
      soc2: soc2 || undefined,
      options: DEFAULT_OPTIONS,
      csvBuResponse: buResponse || undefined,
      csvBuAnswer: buAnswer || undefined,
      csvBuSupportingEvidence: buEvidence || undefined,
    });
  }
  return out;
}

function legacyToForm(): AuditFormQuestion[] {
  return auditQuestions.map((q) => ({
    id: String(q.id),
    category: q.category,
    question: q.question,
    hint: q.hint,
    supportedDocs: undefined,
    soc2: undefined,
    options: q.options,
    csvBuResponse: undefined,
    csvBuAnswer: undefined,
    csvBuSupportingEvidence: undefined,
  }));
}

/** Prefer imported master template; otherwise built-in simplified questions. */
export function getAuditFormQuestions(): AuditFormQuestion[] {
  const fromSheet = getSheetTemplateQuestions();
  if (fromSheet.length > 0) return fromSheet;
  return legacyToForm();
}

export function isUsingSheetTemplate(): boolean {
  return getSheetTemplateQuestions().length > 0;
}
