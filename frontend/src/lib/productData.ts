import { productsAPI } from "@/lib/api";
import type { Product } from "@/types";
import initialData from "@/lib/initialProducts.json";

const retiredProductSlugs = new Set([
  "ivory-ruin-dress",
  "ivory-backless-kaftan",
  "saffron-pleated-dress",
  "tribal-print-slip-dress",
  "ivory-panel-dress",
  "grey-poncho-dress",
  "ivory-flow-dress",
  "white-long-overlay",
  "stone-kimono-overlay",
  "night-print-slip-dress",
  "taupe-backless-dress",
  "rust-hooded-coat",
  "ivory-hooded-wrap-coat",
  "sand-drape-dress",
  "black-drape-dress",
  "black-sheer-skirt-set",
  "black-gold-mini-dress",
  "black-hooded-robe",
  "silver-hooded-vest",
  "black-line-dress",
  "charcoal-sheer-kimono",
  "black-studded-skirt-set",
  "black-lace-skirt-set",
  "brown-wrap-skirt-set",
  "void-walker-trench",
  "asymmetric-drape-dress",
  "tactical-survival-suit",
  "deconstructed-blazer",
  "nomad-cargo-trousers",
  "ritual-wrap-coat",
]);

function visibleProduct(product: Product) {
  if (typeof product.category !== "string") return false;
  return product.is_active !== false && !retiredProductSlugs.has(product.slug);
}

export const fallbackProducts: Product[] = (initialData.products as Product[]).filter(visibleProduct);

let memoryCache: Product[] | null = null;
let fetchPromise: Promise<Product[]> | null = null;
export const CACHE_KEY = "shiv_shakti_products_swr_v5";
export const ADMIN_CACHE_KEY = "shiv_shakti_custom_admin_products_v2";

export async function getAllProducts(forceRefresh = false): Promise<Product[]> {
  return [];
}

function revalidateInBackground() {
  return;
}
