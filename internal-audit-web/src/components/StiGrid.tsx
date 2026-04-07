import Link from "next/link";

export function StiGrid({ stis }: { stis: readonly string[] }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {stis.map((id) => (
        <Link
          key={id}
          href={`/audit/sti/${encodeURIComponent(id)}`}
          className="group relative flex flex-col overflow-hidden rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition hover:border-red-200 hover:shadow-md"
        >
          <span className="pointer-events-none absolute -right-8 -top-8 size-32 rounded-full bg-red-600/[0.07] blur-2xl transition group-hover:bg-red-600/10" />
          <p className="relative text-xs font-semibold uppercase tracking-wide text-slate-500">
            STI
          </p>
          <p className="relative mt-2 font-mono text-xl font-semibold text-slate-900">
            {id}
          </p>
          <p className="relative mt-3 text-sm font-medium text-red-600 opacity-0 transition group-hover:opacity-100">
            Open audit form →
          </p>
        </Link>
      ))}
    </div>
  );
}
