import Link from "next/link";
import { ArrowLeft } from "lucide-react";

export default function Hero() {
    return (
        <section className="relative overflow-hidden bg-stone-50 py-20 lg:py-32">
            <div className="container mx-auto px-4 relative z-10">
                <div className="max-w-3xl mx-auto text-center">
                    <h1 className="text-5xl lg:text-7xl font-extrabold text-slate-900 mb-6 leading-tight drop-shadow-sm">
                        اجعل ذكرياتك <br />
                        <span className="text-orange-600 italic bg-orange-50 px-2 rounded-xl transform -rotate-2 inline-block mx-1">مسموعة</span> ومرئية
                    </h1>

                    <p className="text-xl lg:text-2xl text-slate-700 font-medium mb-10 leading-relaxed max-w-2xl mx-auto">
                        حول كلماتك، مشاعرك، أو أصوات أحبائك إلى لوحة فنية فريدة.
                        <span className="block mt-2 text-slate-900 font-bold">هدية مثالية تخلد اللحظات للأبد.</span>
                    </p>

                    <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                        <Link
                            href="#order-section"
                            className="w-full sm:w-auto px-8 py-4 bg-stone-900 text-white rounded-full text-lg font-semibold flex items-center justify-center gap-2 hover:bg-stone-800 transition-all shadow-xl hover:shadow-2xl transform hover:-translate-y-1"
                        >
                            ابدأ التصميم الآن
                            <ArrowLeft size={20} />
                        </Link>

                        <Link
                            href="#how-it-works"
                            className="w-full sm:w-auto px-8 py-4 bg-white text-stone-900 border border-stone-200 rounded-full text-lg font-semibold hover:bg-stone-50 transition-colors"
                        >
                            كيف يعمل؟
                        </Link>

                        <Link
                            href="/scan"
                            className="w-full sm:w-auto px-8 py-4 bg-orange-600 text-white rounded-full text-lg font-semibold flex items-center justify-center gap-2 hover:bg-orange-700 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-scan-line"><path d="M3 7V5a2 2 0 0 1 2-2h2" /><path d="M17 3h2a2 2 0 0 1 2 2v2" /><path d="M21 17v2a2 2 0 0 1-2 2h-2" /><path d="M7 21H5a2 2 0 0 1-2-2v-2" /><path d="M7 12h10" /></svg>
                            مسح الكود
                        </Link>
                    </div>
                </div>
            </div>

            {/* Decorative background elements */}
            <div className="absolute top-0 left-0 w-full h-full pointer-events-none opacity-30">
                <div className="absolute top-[-10%] right-[-5%] w-96 h-96 bg-orange-100 rounded-full blur-3xl mix-blend-multiply filter"></div>
                <div className="absolute bottom-[-10%] left-[-5%] w-96 h-96 bg-blue-100 rounded-full blur-3xl mix-blend-multiply filter"></div>
            </div>
        </section>
    );
}
