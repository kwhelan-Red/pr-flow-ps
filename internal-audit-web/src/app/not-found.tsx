import Link from "next/link";

export default function NotFound() {
  return (
    <div className="mx-auto max-w-lg px-4 py-20 text-center">
      <p className="text-sm font-semibold uppercase tracking-wide text-slate-500">
        404
      </p>
      <h1 className="mt-2 font-display text-2xl font-semibold text-slate-900">
        Page not found
      </h1>
      <p className="mt-3 text-slate-600">
        That URL does not match anything in this app.
      </p>
      <Link
        href="/"
        className="mt-8 inline-block rounded-lg bg-red-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-red-700"
      >
        Back to home
      </Link>
    </div>
  );
}
