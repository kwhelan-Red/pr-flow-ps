import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { AuditForm } from "@/components/AuditForm";
import { getAuditFormQuestions, isUsingSheetTemplate } from "@/lib/audit-form-questions";
import { getPgeProductBySlug, PGE_PRODUCTS_SOURCE_URL } from "@/pge-products";

type Props = {
  params: Promise<{ slug: string }>;
};

export default async function AuditProductPage({ params }: Props) {
  const { slug: raw } = await params;
  const slug = decodeURIComponent(raw);
  const product = getPgeProductBySlug(slug);

  if (!product) {
    notFound();
  }

  if (product.catalogHref) {
    redirect(product.catalogHref);
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
            <span className="text-slate-700">{product.name}</span>
          </nav>
          <p className="mt-4 text-xs font-semibold uppercase tracking-widest text-slate-500">
            PGE product · Questionnaire
          </p>
          <h1 className="mt-2 font-display text-2xl font-semibold tracking-tight text-slate-900 sm:text-3xl">
            {product.name}
          </h1>
          <p className="mt-2 text-sm text-slate-500">
            Slug: <span className="font-mono text-slate-600">{slug}</span>
          </p>
          <p className="mt-3 text-sm text-slate-600">
            STI-based audits use{" "}
            <Link
              href="/products/secure-flow"
              className="font-medium text-red-600 hover:text-red-700"
            >
              Secure Flow
            </Link>
            . PGE reference:{" "}
            <a
              href={PGE_PRODUCTS_SOURCE_URL}
              className="font-medium text-red-600 underline-offset-2 hover:underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              Source
            </a>
            .
          </p>
          <p className="mt-2 text-sm text-slate-500">
            {isUsingSheetTemplate()
              ? "Questions and hints follow the master template. STI / BU rollup from the sheet is only shown on Secure Flow questionnaires."
              : "Import the master CSV to align questions with the prep template."}
          </p>
        </div>
      </div>

      <div className="mx-auto max-w-3xl px-4 py-10 sm:px-6">
        <AuditForm
          key={`product:${slug}`}
          mode="product"
          entityId={slug}
          displayLabel={product.name}
          questions={questions}
        />
      </div>
    </div>
  );
}
