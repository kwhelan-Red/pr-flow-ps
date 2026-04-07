import Link from "next/link";
import type { PgeProduct } from "@/pge-products";

/** @deprecated Prefer CatalogGrid for the unified catalog; kept for reuse. */
export function ProductGrid({ products }: { products: readonly PgeProduct[] }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3">
      {products.map((p) => (
        <Link
          key={p.slug}
          href={`/audit/product/${encodeURIComponent(p.slug)}`}
          className="group relative flex flex-col overflow-hidden rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition hover:border-red-200 hover:shadow-md"
        >
          <span className="pointer-events-none absolute -right-8 -top-8 size-32 rounded-full bg-red-600/[0.07] blur-2xl transition group-hover:bg-red-600/10" />
          <p className="relative text-xs font-semibold uppercase tracking-wide text-slate-500">
            Product
          </p>
          <p className="relative mt-2 text-base font-semibold leading-snug text-slate-900">
            {p.name}
          </p>
          <p className="relative mt-2 font-mono text-xs text-slate-400">{p.slug}</p>
          <p className="relative mt-4 text-sm font-medium text-red-600 opacity-0 transition group-hover:opacity-100">
            Open audit form →
          </p>
        </Link>
      ))}
    </div>
  );
}
