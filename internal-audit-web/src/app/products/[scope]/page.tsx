import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { StiGrid } from "@/components/StiGrid";
import { isProductScope, productScopeConfig } from "@/data";

type Props = {
  params: Promise<{ scope: string }>;
};

export default async function ProductsByScopePage({ params }: Props) {
  const { scope: raw } = await params;
  const scope = decodeURIComponent(raw);

  if (!isProductScope(scope)) {
    notFound();
  }

  if (scope === "all") {
    redirect("/products");
  }

  const cfg = productScopeConfig[scope];

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
            <Link
              href="/products"
              className="font-medium text-red-600 hover:text-red-700"
            >
              Product catalog
            </Link>
            <span className="mx-2 text-slate-300" aria-hidden>
              /
            </span>
            <span className="text-slate-700">Secure Flow</span>
          </nav>
          <p className="mt-4 text-xs font-semibold uppercase tracking-widest text-slate-500">
            Product
          </p>
          <h1 className="mt-2 font-display text-3xl font-semibold tracking-tight text-slate-900 sm:text-4xl">
            {cfg.title}
          </h1>
          <p className="mt-3 max-w-3xl text-base text-slate-600">
            {cfg.description}
          </p>
          <p className="mt-4 text-sm text-slate-500">
            <span className="font-semibold tabular-nums text-slate-800">
              {productScopeConfig["secure-flow"].stis.length}
            </span>{" "}
            service track identifiers—each card opens the questionnaire for that
            STI.
          </p>
        </div>
      </div>

      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8">
        <StiGrid stis={productScopeConfig["secure-flow"].stis} />
      </div>
    </div>
  );
}
