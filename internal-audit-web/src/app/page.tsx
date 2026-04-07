import Link from "next/link";
import { secureFlowStis } from "@/data";
import { getCatalogProductsSorted } from "@/lib/catalog";

export default function Home() {
  const totalCatalog = getCatalogProductsSorted().length;
  const stiCount = secureFlowStis.length;

  return (
    <>
      <section className="border-b border-slate-200 bg-white">
        <div className="mx-auto max-w-6xl px-4 py-14 sm:px-6 sm:py-20 lg:px-8">
          <div className="max-w-3xl">
            <p className="text-sm font-semibold uppercase tracking-widest text-red-600">
              Red Hat · Internal audit readiness
            </p>
            <h1 className="mt-4 font-display text-4xl font-semibold tracking-tight text-slate-900 sm:text-5xl">
              Structured prep for audits across the product portfolio
            </h1>
            <p className="mt-6 text-lg leading-relaxed text-slate-600">
              Browse one catalog (PGE-aligned lines plus Secure Flow). Each product
              opens the right workflow—STI-based for Secure Flow, questionnaire
              links for the rest. Data stays on your device until you export or
              integrate elsewhere.
            </p>
            <div className="mt-10 flex flex-col gap-3 sm:flex-row sm:items-center">
              <Link
                href="/products"
                className="inline-flex items-center justify-center rounded-lg bg-red-600 px-6 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-red-700"
              >
                View product catalog
              </Link>
            </div>
          </div>

          <dl className="mt-16 grid grid-cols-1 gap-6 border-t border-slate-100 pt-12 sm:grid-cols-2">
            <div className="rounded-xl border border-slate-100 bg-slate-50/80 px-5 py-4">
              <dt className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                Catalog products
              </dt>
              <dd className="mt-2 font-display text-3xl font-semibold tabular-nums text-slate-900">
                {totalCatalog}
              </dd>
            </div>
            <div className="rounded-xl border border-slate-100 bg-slate-50/80 px-5 py-4">
              <dt className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                Secure Flow STIs
              </dt>
              <dd className="mt-2 font-display text-3xl font-semibold tabular-nums text-slate-900">
                {stiCount}
              </dd>
            </div>
          </dl>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-14 sm:px-6 lg:px-8">
        <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm sm:p-10">
          <h2 className="font-display text-xl font-semibold text-slate-900">
            How it works
          </h2>
          <ul className="mt-6 space-y-4 text-slate-600">
            <li className="flex gap-3">
              <span
                className="mt-1 flex size-6 shrink-0 items-center justify-center rounded-full bg-red-100 text-xs font-bold text-red-700"
                aria-hidden
              >
                1
              </span>
              <span>
                Open the <strong className="text-slate-800">product catalog</strong> and
                choose your line—Secure Flow leads to STIs; other products open the
                shared questionnaire.
              </span>
            </li>
            <li className="flex gap-3">
              <span
                className="mt-1 flex size-6 shrink-0 items-center justify-center rounded-full bg-red-100 text-xs font-bold text-red-700"
                aria-hidden
              >
                2
              </span>
              <span>
                Complete the control questionnaire; Secure Flow uses your
                imported master CSV for prompts and BU fields where configured.
              </span>
            </li>
            <li className="flex gap-3">
              <span
                className="mt-1 flex size-6 shrink-0 items-center justify-center rounded-full bg-red-100 text-xs font-bold text-red-700"
                aria-hidden
              >
                3
              </span>
              <span>
                Responses autosave in the browser so you can continue across
                sessions on the same device.
              </span>
            </li>
          </ul>
          <div className="mt-8">
            <Link
              href="/products"
              className="text-sm font-semibold text-red-600 hover:text-red-700"
            >
              Browse the full catalog →
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
