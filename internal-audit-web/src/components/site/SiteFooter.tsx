export function SiteFooter() {
  return (
    <footer className="mt-auto border-t border-slate-200 bg-slate-50">
      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="flex flex-col gap-6 sm:flex-row sm:items-start sm:justify-between">
          <div className="max-w-md">
            <p className="font-display text-sm font-semibold text-slate-900">
              Internal Audit Prep
            </p>
            <p className="mt-2 text-sm leading-relaxed text-slate-600">
              Questionnaire and BU response capture for internal audit
              readiness. Progress is stored locally in your browser unless you
              integrate another backend.
            </p>
          </div>
          <div className="text-sm text-slate-500">
            <p className="font-medium text-slate-700">Data handling</p>
            <p className="mt-1">
              Form answers and evidence are saved in{" "}
              <code className="rounded bg-slate-200/80 px-1.5 py-0.5 text-xs text-slate-800">
                localStorage
              </code>{" "}
              on this device.
            </p>
          </div>
        </div>
        <p className="mt-8 border-t border-slate-200/80 pt-6 text-center text-xs text-slate-500">
          © {new Date().getFullYear()} · For authorized internal use · Template
          data imported from your audit prep master CSV
        </p>
      </div>
    </footer>
  );
}
