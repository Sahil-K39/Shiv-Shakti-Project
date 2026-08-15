"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import type { Product } from "@/types";
import { getAllProducts } from "@/lib/productData";
import ProductCarousel from "@/components/home/ProductCarousel";
import ValuesSection from "@/components/home/ValuesSection";

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    getAllProducts()
      .then((data) => {
        setProducts(data);
        setIsLoading(false);
      })
      .catch(() => setIsLoading(false));
  }, []);

  return (
    <div className="w-full bg-[#fbfaf8] text-black min-h-screen">
      
      {/* 1. Top Section: Information Trio */}
      <section className="w-full max-w-[1400px] mx-auto px-4 md:px-8 py-12 md:py-20 mt-[80px]">
        
        {/* Title as per sketch */}
        <div className="text-center mb-12 md:mb-16">
          <h1 className="text-[28px] md:text-[42px] font-serif uppercase tracking-[0.2em] text-black">
            Shiv Shakti
          </h1>
          <p className="text-[10px] uppercase tracking-[0.3em] text-gray-500 mt-2">
            Home Page
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8">
          {/* About Shiv Shakti */}
          <Link href="/council" className="group flex flex-col h-full bg-white border border-black/10 hover:border-black/30 transition-colors p-8 md:p-12 shadow-sm relative overflow-hidden">
            <h2 className="text-[18px] md:text-[22px] font-light uppercase tracking-[0.15em] mb-4 text-black relative z-10 group-hover:-translate-y-1 transition-transform">
              About Shiv Shakti
            </h2>
            <p className="text-[12px] uppercase tracking-[0.1em] text-gray-500 leading-relaxed relative z-10">
              Avant-garde clothing for the post-apocalyptic era. Deconstructed silhouettes, ritual textures, and ceremonial armor designed for the Council of Light.
            </p>
            <div className="mt-8 text-[10px] font-bold uppercase tracking-[0.2em] text-black border-b border-black/20 pb-1 self-start group-hover:border-black transition-colors relative z-10">
              Read Our Story &rarr;
            </div>
          </Link>

          {/* About Fabric */}
          <Link href="/fabric-selling" className="group flex flex-col h-full bg-white border border-black/10 hover:border-black/30 transition-colors p-8 md:p-12 shadow-sm relative overflow-hidden">
            <h2 className="text-[18px] md:text-[22px] font-light uppercase tracking-[0.15em] mb-4 text-black relative z-10 group-hover:-translate-y-1 transition-transform">
              About Fabric
            </h2>
            <p className="text-[12px] uppercase tracking-[0.1em] text-gray-500 leading-relaxed relative z-10">
              Discover our exclusive fabric collections. Handpicked, high-quality materials including organic cotton, bamboo, and sustainable hemp for wholesale.
            </p>
            <div className="mt-8 text-[10px] font-bold uppercase tracking-[0.2em] text-black border-b border-black/20 pb-1 self-start group-hover:border-black transition-colors relative z-10">
              Explore Fabrics &rarr;
            </div>
          </Link>

          {/* NGO */}
          <Link href="/ngo" className="group flex flex-col h-full bg-black border border-black text-white hover:bg-black/90 transition-colors p-8 md:p-12 shadow-lg relative overflow-hidden">
            <h2 className="text-[18px] md:text-[22px] font-light uppercase tracking-[0.15em] mb-4 text-white relative z-10 group-hover:-translate-y-1 transition-transform">
              NGO
            </h2>
            <p className="text-[12px] uppercase tracking-[0.1em] text-gray-300 leading-relaxed relative z-10">
              Women giving work to women. Empowering local female artisans through high-fashion craftsmanship and fair employment.
            </p>
            <div className="mt-8 text-[10px] font-bold uppercase tracking-[0.2em] text-white border-b border-white/20 pb-1 self-start group-hover:border-white transition-colors relative z-10">
              Support The Cause &rarr;
            </div>
          </Link>
        </div>
      </section>

      {/* 2. Middle Section: Dynamic Product Carousel */}
      <section className="w-full py-16 md:py-24 bg-white border-t border-black/10">
        <div className="max-w-[1400px] mx-auto px-4 md:px-8">
          <div className="text-center mb-12">
            <h2 className="text-[20px] md:text-[28px] font-light uppercase tracking-[0.15em] text-black">
              Products
            </h2>
          </div>
          
          {isLoading ? (
            <div className="flex justify-center py-24">
              <div className="w-8 h-8 border border-black/20 border-t-black animate-spin rounded-full" />
            </div>
          ) : (
            <ProductCarousel products={products} />
          )}
          
          <div className="flex justify-center mt-12">
             <Link
              href="/shop/women"
              className="group relative inline-flex items-center justify-center border border-black bg-black text-white min-h-[48px] px-10 py-4 text-[11px] font-bold uppercase tracking-[0.22em] transition-all hover:bg-white hover:text-black shadow-lg"
            >
              Shop All Products &rarr;
            </Link>
          </div>
        </div>
      </section>

      {/* 3. Bottom Section: Screenshot/Values Section */}
      <ValuesSection />

    </div>
  );
}
