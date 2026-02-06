"use client";
import { useState } from 'react';
import { Plus, Minus } from 'lucide-react';

const faqs = [
    {
        question: "هل الرقائق المستخدمة ذهب حقيقي؟",
        answer: "نحن نستخدم رقائق معدنية فاخرة بلون ذهبي فائق اللمعان مخصصة للأعمال الفنية، لضمان مظهر فخم وسعر مناسب للجميع."
    },
    {
        question: "كيف أسمع الصوت من اللوحة؟",
        answer: "كل لوحة تأتي مزودة بكود ذكي، بمجرد توجيه كاميرا الهاتف إليه، يبدأ المقطع الصوتي الذي اخترته بالعمل."
    }
];

export default function FAQ() {
    const [openIndex, setOpenIndex] = useState<number | null>(null);

    return (
        <section className="max-w-[800px] mx-auto py-16">
            <h2 className="gold-text text-3xl font-bold mb-8 text-center">الأسئلة الشائعة</h2>
            <div className="space-y-4">
                {faqs.map((faq, idx) => (
                    <div key={idx} className="bg-[#1a2431] rounded-xl overflow-hidden">
                        <button
                            onClick={() => setOpenIndex(openIndex === idx ? null : idx)}
                            className="w-full p-5 flex justify-between items-center text-right font-semibold hover:bg-[#233042] transition-colors"
                        >
                            <span>{faq.question}</span>
                            {openIndex === idx ? <Minus size={20} className="text-[#D4AF37]" /> : <Plus size={20} className="text-[#D4AF37]" />}
                        </button>
                        <div
                            className={`transition-all duration-300 ease-in-out overflow-hidden ${openIndex === idx ? 'max-h-40 opacity-100' : 'max-h-0 opacity-0'
                                }`}
                        >
                            <div className="p-5 pt-0 text-gray-300 text-right leading-relaxed border-t border-gray-700/50 mt-2">
                                {faq.answer}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </section>
    );
}
