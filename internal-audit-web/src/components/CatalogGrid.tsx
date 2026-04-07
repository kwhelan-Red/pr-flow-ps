import Link from "next/link";
import type { PgeProduct } from "@/pge-products";
import { getCatalogHref } from "@/lib/catalog";

function CardShell({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div
      className={`group relative flex flex-col overflow-hidden rounded-xl border border-slate-200 bg-white p-6 shadow-sm transition duration-200 hover:border-red-200 hover:shadow-md ${className}`}
    >
      <span className="pointer-events-none absolute -right-10 -top-10 size-36 rounded-full bg-red-600/[0.06] blur-2xl transition group-hover:bg-red-600/10" />
      {children}
    </div>
  );
}

export function CatalogGrid({ products }: { products: PgeProduct[] }) {
  return (
    <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
      {products.map((p) => (
        <Link key={p.slug} href={getCatalogHref(p)} className="block">
          <CardShell>
            <span className="relative text-xs font-semibold uppercase tracking-wide text-slate-500">
              Product
            </span>
            <h2 className="relative mt-2 font-display text-base font-semibold leading-snug text-slate-900">
              {p.name}
            </h2>
            <p className="relative mt-2 font-mono text-xs text-slate-400">
              {p.slug}
            </p>
            <p className="relative mt-4 text-sm font-medium text-red-600 opacity-0 transition group-hover:opacity-100">
              {p.catalogHref
                ? "Open product page →"
                : "Open audit questionnaire →"}
            </p>
          </CardShell>
        </Link>
      ))}
    </div>
  );
}
