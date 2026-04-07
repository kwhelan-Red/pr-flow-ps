import { pgeProducts, type PgeProduct } from "@/pge-products";

export function getCatalogHref(product: PgeProduct): string {
  return product.catalogHref ?? `/audit/product/${encodeURIComponent(product.slug)}`;
}

/** All catalog rows (including Secure Flow), sorted A–Z by display name. */
export function getCatalogProductsSorted(): PgeProduct[] {
  return [...pgeProducts].sort((a, b) =>
    a.name.localeCompare(b.name, "en"),
  );
}
