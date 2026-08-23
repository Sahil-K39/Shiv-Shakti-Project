"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import type { Product } from "@/types";
import { getAllProducts } from "@/lib/productData";
import { getProductImages } from "@/lib/productMedia";
import ValuesSection from "@/components/home/ValuesSection";
import ProductMarquee from "@/components/home/ProductMarquee";
import { formatPriceINR } from "@/lib/pricing";

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    getAllProducts()
      .then((data) => {
        const studioProducts = data.filter(p => {
          if (p.slug.startsWith('aug1_') || p.slug.startsWith('aug8_')) return true;
          if (p.slug.endsWith('_studio')) return true;
          if (p.slug.startsWith('go_')) {
            const numPart = p.slug.replace('go_', '');
            const num = parseInt(numPart);
            if (!isNaN(num) && num >= 48) return true;
          }
          return false;
        });
        setProducts(studioProducts.length > 0 ? studioProducts : data);
        setIsLoading(false);
      })
      .catch(() => setIsLoading(false));
  }, []);

  const featuredProducts = products.slice(0, 8);
  const marqueeProducts = products.slice(8, 28);

  return (
    <div className="w-full bg-[#fbfaf8] text-black min-h-screen">
      
      {/* Hero Video Section */}
      <section className="relative h-[80vh] md:h-screen w-full overflow-hidden bg-black">
        <video 
          autoPlay 
          muted 
          loop 
          playsInline 
          className="absolute inset-0 w-full h-full object-cover"
        >
          <source src="/videos/Complete.mp4" type="video/mp4" />
        </video>
        <div className="absolute inset-0 bg-black/40 z-0" />
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-black/40 z-0" />
        
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center p-6 text-white z-10">
          <h1 className="text-[40px] md:text-[70px] lg:text-[90px] font-light uppercase tracking-[0.15em] mb-4 drop-shadow-lg">
            Shiv Shakti
          </h1>
          <p className="text-[12px] md:text-[14px] uppercase tracking-[0.3em] font-medium opacity-90 mb-8">
            The Core Collection
          </p>
          <Link href="/shop/all" className="border border-white px-8 py-4 text-[12px] uppercase tracking-[0.2em] hover:bg-white hover:text-black transition-colors backdrop-blur-sm">
            Explore Collection
          </Link>
        </div>
      </section>

      {/* 1. The Ethos Grid (Our World) */}
      <section className="w-full max-w-[1400px] mx-auto px-4 md:px-8 pt-[100px] pb-12 md:pb-20">
        <div className="text-center mb-8 md:mb-12">
          <h2 className="text-[20px] md:text-[28px] font-light uppercase tracking-[0.15em] text-black mb-2">
            Our World
          </h2>
          <p className="text-[11px] uppercase tracking-[0.2em] text-gray-500">
            The Philosophy behind Shiv Shakti
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 h-auto md:h-[500px]">
          {/* About Shiv Shakti */}
          <Link href="/council" className="group flex flex-col justify-end h-[350px] md:h-full bg-black transition-colors p-8 shadow-sm relative overflow-hidden">
            <Image
              src="/logos/logo1.webp"
              alt="Shiv Shakti Council"
              fill
              className="object-cover object-center absolute inset-0 z-0 transition-transform duration-700 group-hover:scale-105 opacity-50 group-hover:opacity-40"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent z-0" />
            
            <h3 className="text-[16px] md:text-[20px] font-light uppercase tracking-[0.15em] mb-3 text-white relative z-10 group-hover:-translate-y-1 transition-transform">
              The Council
            </h3>
            <p className="text-[11px] uppercase tracking-[0.1em] text-white/70 leading-relaxed relative z-10 mb-6">
              Deconstructed silhouettes and ceremonial armor designed for the Council of Light.
            </p>
            <div className="text-[10px] font-bold uppercase tracking-[0.2em] text-white border-b border-white/30 pb-1 self-start group-hover:border-white transition-colors relative z-10">
              Read Story
            </div>
          </Link>

          {/* About Fabric */}
          <Link href="/fabric-selling" className="group flex flex-col justify-end h-[350px] md:h-full bg-black transition-colors p-8 shadow-sm relative overflow-hidden">
            <Image
              src="/fabric/fabric-007.jpg"
              alt="Raw Materials and Fabric"
              fill
              className="object-cover object-center absolute inset-0 z-0 transition-transform duration-700 group-hover:scale-105 opacity-50 group-hover:opacity-40"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent z-0" />

            <h3 className="text-[16px] md:text-[20px] font-light uppercase tracking-[0.15em] mb-3 text-white relative z-10 group-hover:-translate-y-1 transition-transform">
              Raw Materials
            </h3>
            <p className="text-[11px] uppercase tracking-[0.1em] text-white/70 leading-relaxed relative z-10 mb-6">
              Organic cotton, bamboo, and sustainable hemp available for wholesale.
            </p>
            <div className="text-[10px] font-bold uppercase tracking-[0.2em] text-white border-b border-white/30 pb-1 self-start group-hover:border-white transition-colors relative z-10">
              Explore Fabrics
            </div>
          </Link>

          {/* NGO */}
          <Link href="/ngo" className="group flex flex-col justify-end h-[350px] md:h-full bg-black transition-colors p-8 shadow-sm relative overflow-hidden">
            <Image
              src="/ngo/artisan-1.jpg"
              alt="Women Artisans"
              fill
              className="object-cover object-center absolute inset-0 z-0 transition-transform duration-700 group-hover:scale-105 opacity-50 group-hover:opacity-40 grayscale"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent z-0" />

            <h3 className="text-[16px] md:text-[20px] font-light uppercase tracking-[0.15em] mb-3 text-white relative z-10 group-hover:-translate-y-1 transition-transform">
              The Initiative
            </h3>
            <p className="text-[11px] uppercase tracking-[0.1em] text-white/70 leading-relaxed relative z-10 mb-6">
              Women empowerment. Empowering artisans through high-fashion craftsmanship.
            </p>
            <div className="text-[10px] font-bold uppercase tracking-[0.2em] text-white border-b border-white/30 pb-1 self-start group-hover:border-white transition-colors relative z-10">
              Support The Cause
            </div>
          </Link>
        </div>
      </section>

      {/* 2. Values Section */}
      <ValuesSection />





      {/* 4. Product Marquee (20 Products) */}
      {!isLoading && marqueeProducts.length > 0 && (
        <ProductMarquee products={marqueeProducts} />
      )}

      {/* 5. New Arrivals (Psylo Style Horizontal Track) */}
      <section className="w-full py-16 md:py-24 bg-[#fbfaf8]">
        <div className="max-w-[1400px] mx-auto px-4 md:px-8">
          <div className="flex justify-between items-end mb-10">
            <div>
              <h2 className="text-[20px] md:text-[28px] font-light uppercase tracking-[0.15em] text-black mb-2">
                New Arrivals
              </h2>
              <p className="text-[11px] uppercase tracking-[0.2em] text-gray-500">
                Latest from the Core Collection
              </p>
            </div>
            <Link
              href="/shop/women"
              className="hidden md:inline-flex text-[11px] font-bold uppercase tracking-[0.2em] text-black border-b border-black pb-1 hover:text-gray-500 transition-colors"
            >
              View All
            </Link>
          </div>
          
          {isLoading ? (
            <div className="flex justify-center py-24">
              <div className="w-8 h-8 border border-black/20 border-t-black animate-spin rounded-full" />
            </div>
          ) : (
            <div className="flex overflow-x-auto pb-8 -mx-4 px-4 md:mx-0 md:px-0 gap-4 md:gap-6 snap-x snap-mandatory scrollbar-hide" style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}>
              {featuredProducts.map((product) => (
                <Link
                  href={`/product/${product.slug}`}
                  key={product.id}
                  className="flex-none w-[70vw] md:w-[calc(25%-18px)] snap-start group"
                >
                  <div className="relative aspect-[3/4] w-full bg-neutral-100 overflow-hidden mb-4 border border-black/5">
                    {getProductImages(product)[0] && (
                      <Image
                        src={getProductImages(product)[0]}
                        alt={product.name}
                        fill
                        className="object-cover object-top transition-transform duration-1000 group-hover:scale-105"
                        sizes="(max-width: 768px) 70vw, 25vw"
                      />
                    )}
                    <div className="absolute inset-0 bg-black/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                  </div>
                  <div className="flex flex-col gap-1">
                    <p className="text-[10px] uppercase tracking-[0.15em] text-gray-500">
                      {product.category}
                    </p>
                    <h3 className="text-[13px] uppercase tracking-[0.1em] font-medium text-black line-clamp-1">
                      {product.name}
                    </h3>
                    <p className="text-[12px] uppercase tracking-[0.15em] text-black mt-1">
                      {formatPriceINR(product.price)}
                    </p>
                  </div>
                </Link>
              ))}
            </div>
          )}

          <div className="mt-8 flex justify-center md:hidden">
            <Link
              href="/shop/women"
              className="inline-flex text-[11px] font-bold uppercase tracking-[0.2em] text-black border-b border-black pb-1"
            >
              View All Arrivals
            </Link>
          </div>
        </div>
      </section>

    </div>
  );
}
// trigger build
