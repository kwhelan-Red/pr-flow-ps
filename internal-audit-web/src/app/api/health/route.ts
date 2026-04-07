import { NextResponse } from "next/server";

/** Load balancers / Kubernetes readiness and liveness probes. */
export function GET() {
  return NextResponse.json(
    { status: "ok", service: "internal-audit-web" },
    {
      status: 200,
      headers: {
        "Cache-Control": "no-store",
      },
    },
  );
}
