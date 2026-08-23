import { productsAPI } from "@/lib/api";
import type { Product } from "@/types";
import initialData from "@/lib/initialProducts.json";
import { parseList } from "@/lib/productMedia";

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
  const hasImages = parseList(product.images).length > 0;
  return hasImages && product.is_active !== false && !retiredProductSlugs.has(product.slug);
}

export const fallbackProducts: Product[] = (initialData.products as unknown as Product[]).filter(visibleProduct);

let memoryCache: Product[] | null = null;
let fetchPromise: Promise<Product[]> | null = null;
export const CACHE_KEY = "shiv_shakti_products_v10";
export const ADMIN_CACHE_KEY = "shiv_shakti_admin_products_v6";
const CACHE_TS_KEY = "shiv_shakti_products_ts";
const CACHE_TTL_MS = 5 * 60 * 1000; // 5 minutes

// Clean up orphaned keys from previous versions
function cleanupOldCacheKeys() {
  if (typeof window === "undefined") return;
  try {
    const keysToRemove: string[] = [];
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith("shiv_shakti_products_swr_")) keysToRemove.push(key);
      if (key && key.startsWith("shiv_shakti_custom_admin_products_")) keysToRemove.push(key);
    }
    keysToRemove.forEach((k) => localStorage.removeItem(k));
  } catch {
    // ignore
  }
}

function isCacheExpired(): boolean {
  if (typeof window === "undefined") return true;
  try {
    const ts = localStorage.getItem(CACHE_TS_KEY);
    if (!ts) return true;
    return Date.now() - parseInt(ts, 10) > CACHE_TTL_MS;
  } catch {
    return true;
  }
}

export async function getAllProducts(forceRefresh = false): Promise<Product[]> {
  if (memoryCache && !forceRefresh) {
    return memoryCache;
  }

  // Clean up old versioned keys on first load
  cleanupOldCacheKeys();

  if (typeof window !== "undefined" && !forceRefresh && !isCacheExpired()) {
    try {
      const saved = sessionStorage.getItem(CACHE_KEY) || localStorage.getItem(CACHE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) {
          memoryCache = parsed.filter(visibleProduct);
          revalidateInBackground();
          return memoryCache;
        }
      }
    } catch {
      // ignore storage errors
    }
  }

  if (fetchPromise) {
    return fetchPromise;
  }

  if (!memoryCache && typeof window !== "undefined" && !forceRefresh) {
    memoryCache = fallbackProducts;
    revalidateInBackground();
    return memoryCache;
  }

  return doFetch();
}

async function doFetch(): Promise<Product[]> {
  if (fetchPromise) return fetchPromise;

  fetchPromise = (async () => {
    try {
      const data = await productsAPI.listAll();
      const valid = (data.products ?? []).filter(visibleProduct);
      if (valid.length > 0) {
        memoryCache = valid;
        if (typeof window !== "undefined") {
          try {
            sessionStorage.setItem(CACHE_KEY, JSON.stringify(valid));
            localStorage.setItem(CACHE_KEY, JSON.stringify(valid));
            localStorage.setItem(CACHE_TS_KEY, Date.now().toString());
          } catch {
            // storage might be full
          }
        }
      }
      return memoryCache ?? fallbackProducts;
    } catch {
      return memoryCache ?? fallbackProducts;
    } finally {
      fetchPromise = null;
    }
  })();

  return fetchPromise;
}

function revalidateInBackground() {
  if (fetchPromise) return;
  doFetch().catch(() => {});
}
