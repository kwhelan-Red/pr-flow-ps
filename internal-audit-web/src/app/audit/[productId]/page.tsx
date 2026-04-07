import { redirect } from "next/navigation";
import { isSecureFlowSti } from "@/data";

type Props = {
  params: Promise<{ productId: string }>;
};

/**
 * Legacy URLs like /audit/BOTA-001 → /audit/sti/BOTA-001 (Secure Flow STIs only).
 */
export default async function AuditLegacyRedirect({ params }: Props) {
  const { productId: raw } = await params;
  const id = decodeURIComponent(raw);

  if (isSecureFlowSti(id)) {
    redirect(`/audit/sti/${encodeURIComponent(id)}`);
  }

  redirect("/products");
}
