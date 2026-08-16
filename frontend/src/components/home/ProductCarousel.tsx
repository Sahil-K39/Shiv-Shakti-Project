"use client";

import { useState, useEffect } from "react";
import Image from "next/image";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import type { Product } from "@/types";
import { formatPriceINR } from "@/lib/pricing";
import { getProductImages } from "@/lib/productMedia";

interface ProductCarouselProps {
  products: Product[];
}

export default function ProductCarousel({ products }: ProductCarouselProps) {
  const [currentIndex, setCurrentIndex] = useState(0);

  // Take exactly 8 products for the carousel (or fewer if we don't have 8)
  const carouselProducts = products.slice(0, 8);

  useEffect(() => {
    if (carouselProducts.length <= 1) return;

    // Rotate every 30 seconds as requested
    const interval = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % carouselProducts.length);
    }, 30000);

    return () => clearInterval(interval);
  }, [carouselProducts.length]);

  if (carouselProducts.length === 0) {
    return null;
  }

  const currentProduct = carouselProducts[currentIndex];

  return (
    <div className="w-full flex flex-col items-center">
      <div className="w-full max-w-[600px] relative aspect-[3/4] overflow-hidden bg-neutral-100 border border-black/10">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentIndex}
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 1.02 }}
            transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
            className="absolute inset-0"
          >
            <Link href={`/product/${currentProduct.slug}`} className="block w-full h-full relative group">
              {getProductImages(currentProduct)[0] && (
                <Image
                  src={getProductImages(currentProduct)[0]}
                  alt={currentProduct.name}
                  fill
                  sizes="(max-width: 768px) 100vw, 600px"
                  className="object-cover object-top hover:scale-105 transition-transform duration-1000"
                />
              )}
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent opacity-80" />
              <div className="absolute bottom-6 left-6 right-6 text-white">
                <p className="text-[10px] uppercase tracking-[0.3em] font-medium opacity-80 mb-2">
                  Featured Product {currentIndex + 1} of {carouselProducts.length}
                </p>
                <h3 className="text-[20px] md:text-[28px] font-light uppercase tracking-[0.15em] mb-2 leading-tight">
                  {currentProduct.name}
                </h3>
                <p className="text-[12px] uppercase tracking-[0.2em] font-medium">
                  {formatPriceINR(currentProduct.price)}
                </p>
              </div>
            </Link>
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Indicators */}
      <div className="flex items-center gap-2 md:gap-3 mt-8">
        {carouselProducts.map((_, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => setCurrentIndex(idx)}
            aria-label={`Go to product ${idx + 1}`}
            className={`transition-all duration-300 rounded-full h-[3px] md:h-1 ${
              idx === currentIndex ? "w-10 md:w-12 bg-black" : "w-3 md:w-4 bg-black/20 hover:bg-black/40"
            }`}
          />
        ))}
      </div>
      
    </div>
  );
}
