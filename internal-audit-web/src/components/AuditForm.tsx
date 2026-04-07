"use client";

import {
  startTransition,
  useCallback,
  useEffect,
  useMemo,
  useState,
} from "react";
import { LinkifiedText } from "@/components/LinkifiedText";
import { enrichHintWithKnownLinks } from "@/lib/hint-link-enrichment";
import type { AuditFormQuestion } from "@/types/audit-form";

type PersistedPayload = {
  answers: Record<string, string>;
  evidence: Record<string, string>;
  updatedAt: string;
};

function storageKey(mode: "sti" | "product", entityId: string) {
  return `internal-audit:2026:${mode}:${entityId}`;
}

function loadState(mode: "sti" | "product", entityId: string): PersistedPayload {
  if (typeof window === "undefined") {
    return { answers: {}, evidence: {}, updatedAt: "" };
  }
  try {
    let raw = localStorage.getItem(storageKey(mode, entityId));
    if (!raw && mode === "sti") {
      raw = localStorage.getItem(`internal-audit:2026:${entityId}`);
    }
    if (!raw) return { answers: {}, evidence: {}, updatedAt: "" };
    const parsed = JSON.parse(raw) as PersistedPayload;
    return {
      answers: parsed.answers ?? {},
      evidence: parsed.evidence ?? {},
      updatedAt: parsed.updatedAt ?? "",
    };
  } catch {
    return { answers: {}, evidence: {}, updatedAt: "" };
  }
}

function saveState(
  mode: "sti" | "product",
  entityId: string,
  payload: PersistedPayload,
) {
  localStorage.setItem(storageKey(mode, entityId), JSON.stringify(payload));
}

function norm(s: string) {
  return s.trim().toLowerCase().replace(/\s+/g, " ");
}

function matchCsvToOption(
  raw: string | undefined,
  options: readonly string[],
): string | undefined {
  if (!raw?.trim()) return undefined;
  const firstLine = raw.trim().split(/\r?\n/)[0]?.trim() ?? raw.trim();
  const n = norm(firstLine);
  for (const opt of options) {
    if (norm(opt) === n) return opt;
  }
  for (const opt of options) {
    if (n.includes(norm(opt)) || norm(opt).includes(n)) return opt;
  }
  return undefined;
}

export function AuditForm({
  mode,
  entityId,
  displayLabel,
  questions,
  applyCsvBuPrefill = false,
}: {
  mode: "sti" | "product";
  entityId: string;
  displayLabel: string;
  questions: AuditFormQuestion[];
  applyCsvBuPrefill?: boolean;
}) {
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [evidence, setEvidence] = useState<Record<string, string>>({});
  const [hydrated, setHydrated] = useState(false);
  const [status, setStatus] = useState<"idle" | "saved">("idle");

  const questionIds = useMemo(
    () => questions.map((q) => String(q.id)).join(","),
    [questions],
  );

  useEffect(() => {
    const s = loadState(mode, entityId);
    const nextAnswers: Record<string, string> = {};
    const nextEvidence: Record<string, string> = {};

    for (const q of questions) {
      const qid = String(q.id);
      const savedA = (s.answers[qid] ?? "").trim();
      const savedE = (s.evidence[qid] ?? "").trim();

      let a = savedA;
      if (!a && applyCsvBuPrefill) {
        const fromAnswer = matchCsvToOption(q.csvBuAnswer, q.options);
        const fromResponse = matchCsvToOption(q.csvBuResponse, q.options);
        a = fromAnswer ?? fromResponse ?? "";
      }

      let e = savedE;
      if (!e && applyCsvBuPrefill && q.csvBuSupportingEvidence?.trim()) {
        e = q.csvBuSupportingEvidence.trim();
      }

      nextAnswers[qid] = a;
      nextEvidence[qid] = e;
    }

    startTransition(() => {
      setAnswers(nextAnswers);
      setEvidence(nextEvidence);
      setHydrated(true);
    });
  }, [mode, entityId, questionIds, applyCsvBuPrefill, questions]);

  const persist = useCallback(
    (nextAnswers: Record<string, string>, nextEvidence: Record<string, string>) => {
      const payload: PersistedPayload = {
        answers: nextAnswers,
        evidence: nextEvidence,
        updatedAt: new Date().toISOString(),
      };
      saveState(mode, entityId, payload);
    },
    [mode, entityId],
  );

  useEffect(() => {
    if (!hydrated) return;
    persist(answers, evidence);
  }, [answers, evidence, hydrated, persist]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    persist(answers, evidence);
    setStatus("saved");
    window.setTimeout(() => setStatus("idle"), 2500);
  };

  const scopeHint = mode === "sti" ? "Secure Flow STI" : "product";

  return (
    <form
      onSubmit={handleSubmit}
      className="mx-auto max-w-3xl space-y-8 pb-24"
    >
      {questions.map((q, index) => {
        const qid = String(q.id);
        const hasCsvBuContent = Boolean(
          q.csvBuAnswer?.trim() ||
            q.csvBuResponse?.trim() ||
            q.csvBuSupportingEvidence?.trim(),
        );

        const hintForDisplay = enrichHintWithKnownLinks(q.hint);
        const docsForDisplay = q.supportedDocs
          ? enrichHintWithKnownLinks(q.supportedDocs)
          : "";

        return (
          <section
            key={`${qid}-${index}`}
            className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
          >
            <p className="text-xs font-semibold tabular-nums text-slate-400">
              #{qid}
            </p>
            <p className="mt-1 text-xs font-semibold uppercase tracking-wider text-red-600">
              {q.category}
            </p>
            {q.soc2 ? (
              <p className="mt-1 text-xs leading-snug text-slate-500">{q.soc2}</p>
            ) : null}
            <div className="mt-3 text-lg font-medium leading-snug text-slate-900">
              <LinkifiedText text={q.question} />
            </div>

            {hintForDisplay.trim() ? (
              <aside className="mt-4 rounded-lg border border-emerald-200 bg-emerald-50/90 px-3 py-3">
                <p className="text-[11px] font-semibold uppercase tracking-wide text-emerald-900">
                  Hints / guidance (from template)
                </p>
                <div className="mt-2 text-sm leading-relaxed text-slate-700">
                  <LinkifiedText text={hintForDisplay} />
                </div>
              </aside>
            ) : null}

            {mode === "sti" && hasCsvBuContent ? (
              <aside className="relative z-[1] mt-4 rounded-lg border border-emerald-200 bg-emerald-50/80 px-3 py-3">
                <p className="text-[11px] font-semibold uppercase tracking-wide text-emerald-800">
                  BU responses (from CSV · Secure Flow)
                </p>
                <dl className="mt-2 space-y-2 text-sm">
                  {q.csvBuAnswer?.trim() ? (
                    <div>
                      <dt className="text-xs text-slate-500">BU Answer</dt>
                      <dd className="text-slate-800">
                        <LinkifiedText text={q.csvBuAnswer} />
                      </dd>
                    </div>
                  ) : null}
                  {q.csvBuResponse?.trim() ? (
                    <div>
                      <dt className="text-xs text-slate-500">BU Response</dt>
                      <dd className="text-slate-800">
                        <LinkifiedText text={q.csvBuResponse} />
                      </dd>
                    </div>
                  ) : null}
                  {q.csvBuSupportingEvidence?.trim() ? (
                    <div>
                      <dt className="text-xs text-slate-500">
                        BU Supporting Evidence
                      </dt>
                      <dd className="text-slate-800">
                        <LinkifiedText text={q.csvBuSupportingEvidence} />
                      </dd>
                    </div>
                  ) : null}
                </dl>
              </aside>
            ) : null}

            {docsForDisplay.trim() ? (
              <aside className="mt-4 rounded-lg border border-slate-200 bg-slate-50 px-3 py-3">
                <p className="text-[11px] font-semibold uppercase tracking-wide text-slate-600">
                  Supported documents — good to have for readiness
                </p>
                <div className="mt-2 text-sm leading-relaxed text-slate-600">
                  <LinkifiedText text={docsForDisplay} />
                </div>
              </aside>
            ) : null}

            <fieldset className="mt-5">
              <legend className="sr-only">Response for question {qid}</legend>
              <div className="flex flex-wrap gap-3">
                {q.options.map((opt) => {
                  const inputId = `q${qid}-${opt.replace(/\s+/g, "-")}`;
                  return (
                    <label
                      key={opt}
                      htmlFor={inputId}
                      className={`inline-flex cursor-pointer items-center gap-2 rounded-lg border px-3 py-2 text-sm transition-colors ${
                        answers[qid] === opt
                          ? "border-red-600 bg-red-50 text-red-900"
                          : "border-slate-200 bg-white text-slate-700 hover:border-slate-300"
                      }`}
                    >
                      <input
                        id={inputId}
                        type="radio"
                        name={`question-${qid}`}
                        value={opt}
                        checked={answers[qid] === opt}
                        onChange={() =>
                          setAnswers((prev) => ({ ...prev, [qid]: opt }))
                        }
                        className="size-4 accent-red-600"
                      />
                      {opt}
                    </label>
                  );
                })}
              </div>
            </fieldset>

            <label className="mt-5 block text-sm font-medium text-slate-700">
              BU supporting evidence, links, or comments
              <textarea
                className="mt-2 min-h-[100px] w-full resize-y rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 placeholder:text-slate-400 focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/20"
                placeholder="Links, ticket IDs, documents, or notes…"
                value={evidence[qid] ?? ""}
                onChange={(e) =>
                  setEvidence((prev) => ({ ...prev, [qid]: e.target.value }))
                }
              />
            </label>
          </section>
        );
      })}

      <div className="sticky bottom-0 z-10 -mx-4 flex flex-col gap-3 border-t border-slate-200 bg-slate-50/95 px-4 py-4 backdrop-blur sm:flex-row sm:items-center sm:justify-between">
        <p className="text-xs text-slate-500">
          Autosave ({scopeHint}):{" "}
          <span className="font-medium text-slate-700">{displayLabel}</span>
          {" · "}
          {questions.length} question{questions.length === 1 ? "" : "s"}
          {applyCsvBuPrefill
            ? " · CSV BU fields prefill when local answers are empty"
            : ""}
        </p>
        <div className="flex items-center gap-3">
          {status === "saved" && (
            <span className="text-sm font-medium text-emerald-700">
              Saved locally
            </span>
          )}
          <button
            type="submit"
            className="rounded-lg bg-red-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-red-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-red-600 focus-visible:ring-offset-2"
          >
            Save &amp; submit audit
          </button>
        </div>
      </div>
    </form>
  );
}
