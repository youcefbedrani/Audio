import Hero from "@/components/Hero";
import OrderSection from "@/components/OrderSection";
import { Mic, ScanLine, Image as ImageIcon, Gift, Truck, ShieldCheck } from "lucide-react";
import Link from "next/link";
import Image from "next/image";

export default function Home() {
  return (
    <main className="min-h-screen bg-stone-50">
      <Hero />

      {/* How it Works Section */}
      <section id="how-it-works" className="py-24 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-stone-900 mb-4">كيف تعمل؟</h2>
            <p className="text-stone-600 max-w-2xl mx-auto">
              خطوات بسيطة تفصلك عن هديتك المثالية
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-12 max-w-5xl mx-auto">
            <div className="flex flex-col items-center text-center group">
              <div className="w-20 h-20 bg-stone-100 rounded-2xl flex items-center justify-center mb-6 text-stone-900 group-hover:bg-stone-900 group-hover:text-white transition-colors duration-300">
                <Mic size={32} />
              </div>
              <h3 className="text-xl font-bold mb-3">1. سجل رسالتك</h3>
              <p className="text-stone-500 leading-relaxed">
                سجل رسالة صوتية، دعاء، أو ارفع أغنية مفضلة مباشرة من هاتفك
              </p>
            </div>

            <div className="flex flex-col items-center text-center group">
              <div className="w-20 h-20 bg-stone-100 rounded-2xl flex items-center justify-center mb-6 text-stone-900 group-hover:bg-stone-900 group-hover:text-white transition-colors duration-300">
                <ImageIcon size={32} />
              </div>
              <h3 className="text-xl font-bold mb-3">2. اختر التصميم</h3>
              <p className="text-stone-500 leading-relaxed">
                اختر شكل الإطار، الألوان، ونوع الموجة الصوتية التي تناسب ذوقك
              </p>
            </div>

            <div className="flex flex-col items-center text-center group">
              <div className="w-20 h-20 bg-stone-100 rounded-2xl flex items-center justify-center mb-6 text-stone-900 group-hover:bg-stone-900 group-hover:text-white transition-colors duration-300">
                <ScanLine size={32} />
              </div>
              <h3 className="text-xl font-bold mb-3">3. استلم واستمع</h3>
              <p className="text-stone-500 leading-relaxed">
                يصلك الإطار لباب المنزل، امسح الموجة بتطبيقنا واسترجع الذكريات
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Order Section (Replaces Gallery) */}
      <section className="py-24 bg-stone-50" id="order-section">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-stone-900 mb-4">صمم إطارك الفني الآن</h2>
            <p className="text-stone-600">اطلب في دقائق، والدفع عند الاستلام</p>
          </div>

          <OrderSection />
        </div>
      </section>

      {/* Trust & Benefits */}
      <section className="py-20 bg-white border-t border-stone-100">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="flex items-center gap-4 p-6 bg-stone-50 rounded-2xl">
              <div className="p-3 bg-white rounded-full shadow-sm text-stone-900">
                <Truck size={24} />
              </div>
              <div>
                <h4 className="font-bold text-lg">توصيل 58 ولاية</h4>
                <p className="text-stone-500 text-sm">شحن سريع وآمن لكل الجزائر</p>
              </div>
            </div>

            <div className="flex items-center gap-4 p-6 bg-stone-50 rounded-2xl">
              <div className="p-3 bg-white rounded-full shadow-sm text-stone-900">
                <ShieldCheck size={24} />
              </div>
              <div>
                <h4 className="font-bold text-lg">دفع عند الاستلام</h4>
                <p className="text-stone-500 text-sm">عاين منتجك قبل الدفع</p>
              </div>
            </div>

            <div className="flex items-center gap-4 p-6 bg-stone-50 rounded-2xl">
              <div className="p-3 bg-white rounded-full shadow-sm text-stone-900">
                <Gift size={24} />
              </div>
              <div>
                <h4 className="font-bold text-lg">تغليف هدايا فاخر</h4>
                <p className="text-stone-500 text-sm">جاهز للإهداء مباشرة</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <footer className="bg-stone-900 text-white py-12">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-2xl font-bold mb-6">إطار الصوت الفني</h2>
          <p className="text-stone-400 mb-8">نحول أصواتكم إلى فن خالد</p>
          <div className="text-stone-600 text-sm">
            &copy; 2024 Audio Art Frame. All rights reserved.
          </div>
        </div>
      </footer>
    </main>
  );
}