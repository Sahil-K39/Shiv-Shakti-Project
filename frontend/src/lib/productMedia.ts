import type { Product } from "@/types";
import { getRandomProductImage } from "@/lib/siteImageProvider";

const productImageAliases: Record<string, string[]> = {};

const categoryFallbacks: Record<string, string[]> = {
  shakti: [
    "/final-products/go01/go01-01.webp",
    "/final-products/go02/go02-01.webp",
  ],
  shiva: [
    "/final-products/go15/go15-01.webp",
    "/final-products/go16/go16-01.webp",
  ],
};

const swatches: Record<string, string> = {
  ash: "#d8d8d2",
  charcoal: "#2d2d2d",
  "desert storm": "#8d8376",
  obsidian: "#090909",
  stone: "#8f8b82",
  "void black": "#050505",
};

export function toWebp(url: string | null | undefined): string {
  if (!url) return "";
  if (url.startsWith("/final-products/") || url.startsWith("/logos/")) {
    return url.replace(/\.png$/i, ".webp");
  }
  return url;
}

export function parseList(value: string[] | string | null | undefined): string[] {
  if (Array.isArray(value)) return value.filter(Boolean).map(toWebp);
  if (!value) return [];

  try {
    const parsed = JSON.parse(value);
    return (Array.isArray(parsed) ? parsed.filter(Boolean) : []).map(toWebp);
  } catch {
    return value ? [toWebp(value)] : [];
  }
}

export function getProductImages(product: Product): string[] {
  // The user requested to remove all product images from the website
  return ["/placeholder.svg"];
}

export function getCartItemImage(images: string[] | string | null | undefined) {
  return "/placeholder.svg";
}

export function getCategoryFallbackImage(category: string | null | undefined) {
  return "/placeholder.svg";
}

export function getColorSwatch(color: string) {
  return swatches[color.toLowerCase()] ?? "#777";
}
