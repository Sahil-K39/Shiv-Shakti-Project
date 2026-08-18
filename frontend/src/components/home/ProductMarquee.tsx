import Link from "next/link";
import Image from "next/image";
import type { Product } from "@/types";
import { getProductImages } from "@/lib/productMedia";
import { formatPriceINR } from "@/lib/pricing";

export default function ProductMarquee({ products }: { products: Product[] }) {
  if (!products || products.length === 0) return null;

  // Duplicate the array to create a seamless infinite scroll
  const marqueeItems = [...products, ...products];

  return (
    <section className="w-full bg-[#fbfaf8] pt-12 pb-4 overflow-hidden">
      <div className="flex w-max animate-marquee hover:[animation-play-state:paused] items-center">
        {marqueeItems.map((product, idx) => (
          <Link
            href={`/product/${product.slug}`}
            key={`${product.id}-${idx}`}
            className="w-[180px] md:w-[240px] flex-none px-3 group"
          >
            <div className="relative aspect-[3/4] w-full bg-neutral-100 overflow-hidden mb-3 border border-black/5">
              {getProductImages(product)[0] && (
                <Image
                  src={getProductImages(product)[0]}
                  alt={product.name}
                  fill
                  className="object-cover object-top transition-transform duration-1000 group-hover:scale-105"
                  sizes="(max-width: 768px) 180px, 240px"
                />
              )}
              <div className="absolute inset-0 bg-black/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            </div>
            <div className="flex flex-col gap-1 items-center text-center">
              <h3 className="text-[11px] uppercase tracking-[0.1em] font-medium text-black line-clamp-1">
                {product.name}
              </h3>
              <p className="text-[10px] uppercase tracking-[0.15em] text-gray-500">
                {formatPriceINR(product.price)}
              </p>
            </div>
          </Link>
        ))}
      </div>
    </section>
  );
}
