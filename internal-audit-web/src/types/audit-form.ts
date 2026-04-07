/** One row in the audit UI (sheet template or legacy fallback). */
export type AuditFormQuestion = {
  id: string;
  category: string;
  question: string;
  hint: string;
  supportedDocs?: string;
  soc2?: string;
  options: readonly string[];
  /**
   * From CSV (BU Answer / BU Response). Used as Secure Flow form prefill only.
   * Must match an entry in `options` after normalization when used as radio value.
   */
  csvBuAnswer?: string;
  csvBuResponse?: string;
  csvBuSupportingEvidence?: string;
};
