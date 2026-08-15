export default function ValuesSection() {
  return (
    <div className="w-full bg-white border-t border-black/10 py-16 md:py-24">
      <div className="max-w-[1400px] mx-auto px-4 md:px-8 grid grid-cols-1 md:grid-cols-3 gap-12 md:gap-8">
        
        {/* Sustainable */}
        <div className="flex flex-col items-center text-center px-4">
          <div className="mb-6 w-12 h-12 flex items-center justify-center text-black/80">
            {/* 3 Leaves Circle Icon */}
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" className="w-full h-full">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z" />
              <path d="M12 6c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6zm0 10c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4z" />
              <path d="M12 9c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z" />
            </svg>
          </div>
          <h4 className="text-[14px] font-bold text-black mb-3 tracking-wide">
            Sustainable
          </h4>
          <p className="text-[13px] text-gray-500 leading-relaxed font-light">
            Organic cotton, bamboo and hemp. Made to last.
          </p>
        </div>

        {/* Handmade */}
        <div className="flex flex-col items-center text-center px-4">
          <div className="mb-6 w-12 h-12 flex items-center justify-center text-black/80">
            {/* Hand with Heart Icon */}
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" className="w-full h-full">
              <path d="M18 11V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v0" />
              <path d="M14 4a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v0" />
              <path d="M10 4a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v0" />
              <path d="M6 11V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v0" />
              <path d="M18 11c0 3.31-2.69 6-6 6s-6-2.69-6-6" />
              <path d="M9.5 13.5l2.5 2.5 2.5-2.5a1.5 1.5 0 0 0-2.12-2.12L12 11.88l-.38-.38a1.5 1.5 0 0 0-2.12 2.12z" />
            </svg>
          </div>
          <h4 className="text-[14px] font-bold text-black mb-3 tracking-wide">
            Handmade
          </h4>
          <p className="text-[13px] text-gray-500 leading-relaxed font-light">
            Cut, sewn and finished by hand in our Bali workshop.
          </p>
        </div>

        {/* Upcycled */}
        <div className="flex flex-col items-center text-center px-4">
          <div className="mb-6 w-12 h-12 flex items-center justify-center text-black/80">
            {/* Shirt with recycle arrows Icon */}
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" className="w-full h-full">
              <path d="M20 7h-3V4c0-1.1-.9-2-2-2H9c-1.1 0-2 .9-2 2v3H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2zM9 4h6v3H9V4zm11 16H4V9h16v11z" />
              <path d="M12 12v3l3-3-3-3v3c-1.66 0-3 1.34-3 3 0 .41.08.8.23 1.16l1.09-1.09c-.04-.23-.09-.47-.09-.73 0-1.1.9-2 2-2z" />
            </svg>
          </div>
          <h4 className="text-[14px] font-bold text-black mb-3 tracking-wide">
            Upcycled
          </h4>
          <p className="text-[13px] text-gray-500 leading-relaxed font-light max-w-sm">
            Offcuts and leftover fabrics are reused across collections. Nothing wasted.
          </p>
        </div>

      </div>
    </div>
  );
}
