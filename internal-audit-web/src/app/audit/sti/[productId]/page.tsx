import Link from "next/link";
import { notFound } from "next/navigation";
import { AuditForm } from "@/components/AuditForm";
import { isSecureFlowSti } from "@/data";
import { getAuditFormQuestions, isUsingSheetTemplate } from "@/lib/audit-form-questions";

type Props = {
  params: Promise<{ productId: string }>;
};

export default async function AuditStiPage({ params }: Props) {
  const { productId: raw } = await params;
  const sti = decodeURIComponent(raw);

  if (!isSecureFlowSti(sti)) {
    notFound();
  }

  const questions = getAuditFormQuestions();

  return (
    <div className="min-h-full">
      <div className="border-b border-slate-200 bg-white">
        <div className="mx-auto max-w-3xl px-4 py-8 sm:px-6">
          <nav className="text-sm text-slate-500">
            <Link href="/" className="font-medium text-red-600 hover:text-red-700">
              Home
            </Link>
            <span className="mx-2 text-slate-300">/</span>
            <Link
              href="/products"
              className="font-medium text-red-600 hover:text-red-700"
            >
              Product catalog
            </Link>
            <span className="mx-2 text-slate-300">/</span>
            <Link
              href="/products/secure-flow"
              className="font-medium text-red-600 hover:text-red-700"
            >
              Secure Flow
            </Link>
            <span className="mx-2 text-slate-300">/</span>
            <span className="text-slate-700">{sti}</span>
          </nav>
          <p className="mt-4 text-xs font-semibold uppercase tracking-widest text-red-600">
            Secure Flow · STI questionnaire
          </p>
          <h1 className="mt-2 font-display text-3xl font-semibold tracking-tight text-slate-900">
            <span className="text-slate-500">STI</span>{" "}
            <span className="font-mono text-slate-900">{sti}</span>
          </h1>
          <p className="mt-3 text-sm leading-relaxed text-slate-600">
            {isUsingSheetTemplate()
              ? "Questions, hints, and BU fields follow the imported Internal Audit Prep master CSV where configured."
              : "Run npm run import-audit-sheet with your CSV, or a built-in question set is used."}{" "}
            Progress is saved in this browser.
          </p>
        </div>
      </div>

      <div className="mx-auto max-w-3xl px-4 py-10 sm:px-6">
        <AuditForm
          key={`sti:${sti}`}
          mode="sti"
          entityId={sti}
          displayLabel={`STI ${sti}`}
          questions={questions}
          applyCsvBuPrefill={isUsingSheetTemplate()}
        />
      </div>
    </div>
  );
}
