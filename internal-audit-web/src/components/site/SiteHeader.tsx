import Link from "next/link";

const nav = [
  { href: "/", label: "Home" },
  { href: "/products", label: "Product catalog" },
] as const;

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-50 border-b border-slate-200/80 bg-white/95 shadow-sm backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between gap-6 px-4 sm:px-6 lg:px-8">
        <Link href="/" className="group flex shrink-0 items-center gap-3">
          <span
            className="flex size-9 items-center justify-center rounded-md font-display text-lg font-bold text-white shadow-sm"
            style={{ background: "linear-gradient(135deg, #cc0000 0%, #ee0000 100%)" }}
            aria-hidden
          >
            IA
          </span>
          <span className="flex flex-col leading-tight">
            <span className="font-display text-base font-semibold tracking-tight text-slate-900 group-hover:text-slate-700">
              Internal Audit Prep
            </span>
            <span className="hidden text-xs font-medium text-slate-500 sm:block">
              Red Hat · Business units
            </span>
          </span>
        </Link>

        <nav
          className="flex items-center gap-1 sm:gap-2"
          aria-label="Primary"
        >
          {nav.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className="rounded-md px-3 py-2 text-sm font-medium text-slate-600 transition hover:bg-slate-100 hover:text-slate-900"
            >
              {label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
