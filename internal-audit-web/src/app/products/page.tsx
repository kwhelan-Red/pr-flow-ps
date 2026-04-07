import Link from "next/link";
import { CatalogGrid } from "@/components/CatalogGrid";
import { getCatalogProductsSorted } from "@/lib/catalog";
import { PGE_PRODUCTS_SOURCE_URL } from "@/pge-products";

export default function ProductsCatalogPage() {
  const products = getCatalogProductsSorted();

  return (
    <div className="min-h-full">
      <div className="border-b border-slate-200 bg-white">
        <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8">
          <nav className="text-sm text-slate-500">
            <Link href="/" className="font-medium text-red-600 hover:text-red-700">
              Home
            </Link>
            <span className="mx-2 text-slate-300" aria-hidden>
              /
            </span>
            <span className="text-slate-700">Product catalog</span>
          </nav>
          <h1 className="mt-4 font-display text-3xl font-semibold tracking-tight text-slate-900 sm:text-4xl">
            Product catalog
          </h1>
          <p className="mt-3 max-w-3xl text-base leading-relaxed text-slate-600">
            Alphabetical catalog aligned with Products &amp; Global Engineering,
            including Secure Flow (opens the STI list, then the questionnaire per
            STI). Official PGE directory:{" "}
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
          <p className="mt-4 text-sm text-slate-500">
            <span className="font-semibold tabular-nums text-slate-800">
              {products.length}
            </span>{" "}
            products — update names in{" "}
            <code className="rounded bg-slate-100 px-1.5 py-0.5 text-xs text-slate-700">
              src/pge-products.ts
            </code>
            .
          </p>
        </div>
      </div>

      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8">
        <CatalogGrid products={products} />
      </div>
    </div>
  );
}
