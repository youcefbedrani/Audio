import Image from 'next/image';

export default function Hero() {
    return (
        <section className="min-h-screen flex flex-col justify-center items-center text-center bg-[radial-gradient(circle_at_center,_#1c2533_0%,_#111822_100%)]">
            <h1 className="gold-text text-4xl md:text-6xl font-bold mb-4 leading-tight">
                بصمة صوتك.. تحفةٌ تلمعُ للأبد
            </h1>
            <p className="text-lg md:text-xl max-w-2xl mb-8 opacity-90">
                حوّل مشاعرك إلى فن مرئي يُسمع بالقلب ويُرى بالعين عبر أرقى الرقائق الذهبية.
            </p>

            <div className="relative w-full max-w-[550px] mt-8 mb-10 transition-transform hover:scale-105 duration-500">
                <Image
                    src="/assets/product-hero.png"
                    alt="لوحة Rouisia Voice"
                    width={550}
                    height={550}
                    className="w-full h-auto drop-shadow-[0_25px_35px_rgba(0,0,0,0.6)]"
                    priority
                />
            </div>

            <a
                href="#customization-section"
                className="bg-[linear-gradient(45deg,_#BF953F,_#FCF6BA,_#AA771C)] text-black px-12 py-4 rounded-full text-xl font-extrabold shadow-[0_10px_30px_rgba(170,119,28,0.4)] hover:shadow-[0_15px_40px_rgba(170,119,28,0.6)] transition-all transform hover:-translate-y-1"
            >
                صمم هديتك الآن
            </a>
        </section>
    );
}
