"use client";

import { useEffect } from "react";

/**
 * Catches errors in the root layout. Must define its own <html> / <body>.
 * @see https://nextjs.org/docs/app/api-reference/file-conventions/error#global-error
 */
export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <html lang="en">
      <body className="flex min-h-screen flex-col items-center justify-center bg-slate-50 px-4 font-sans text-slate-800">
        <h1 className="text-xl font-semibold text-slate-900">
          Application error
        </h1>
        <p className="mt-2 max-w-md text-center text-slate-600">
          The layout failed to load. Try reloading the page.
        </p>
        <button
          type="button"
          onClick={() => reset()}
          className="mt-6 rounded-lg bg-red-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-red-700"
        >
          Try again
        </button>
      </body>
    </html>
  );
}
