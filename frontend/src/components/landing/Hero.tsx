import Image from 'next/image';

import Link from 'next/link';
import { Scan } from 'lucide-react';

export default function Hero() {
    return (
        <section className="min-h-screen flex flex-col justify-center items-center text-center bg-[radial-gradient(circle_at_center,_#1c2533_0%,_#111822_100%)] px-4 py-12">

            {/* App Logo */}
            <div className="mb-6 animate-fade-in">
                <Image
                    src="/icon.png"
                    alt="Logo"
                    width={120}
                    height={120}
                    className="w-24 h-24 md:w-32 md:h-32 object-contain drop-shadow-[0_0_15px_rgba(255,215,60,0.3)]"
                />
            </div>

            <h1 className="gold-text text-4xl md:text-6xl font-bold mb-4 leading-tight">
                بصمة صوتك.. تحفةٌ تلمعُ للأبد
            </h1>
            <p className="text-lg md:text-xl max-w-2xl mb-8 opacity-90 text-gray-300">
                حوّل مشاعرك إلى فن مرئي يُسمع بالقلب ويُرى بالعين عبر أرقى الرقائق الذهبية.
            </p>

            <div className="relative w-full max-w-[550px] mt-4 mb-10 transition-transform hover:scale-105 duration-500">
                <Image
                    src="/assets/product-hero.png"
                    alt="لوحة Rouisia Voice"
                    width={550}
                    height={550}
                    className="w-full h-auto drop-shadow-[0_25px_35px_rgba(0,0,0,0.6)]"
                    priority
                />
            </div>

            <div className="flex flex-col sm:flex-row items-center gap-6 w-full justify-center">
                <a
                    href="#customization-section"
                    className="bg-[linear-gradient(45deg,_#BF953F,_#FCF6BA,_#AA771C)] text-black px-10 py-4 rounded-full text-xl font-extrabold shadow-[0_10px_30px_rgba(170,119,28,0.4)] hover:shadow-[0_15px_40px_rgba(170,119,28,0.6)] transition-all transform hover:-translate-y-1 w-full sm:w-auto"
                >
                    صمم هديتك الآن
                </a>

                <Link
                    href="/scan"
                    className="px-10 py-4 rounded-full text-xl font-bold border-2 border-[#D4AF37] text-[#D4AF37] hover:bg-[#D4AF37]/10 transition-all flex items-center justify-center gap-2 w-full sm:w-auto"
                >
                    <Scan className="w-6 h-6" />
                    مسح اللوحة
                </Link>
            </div>
        </section>
    );
}
