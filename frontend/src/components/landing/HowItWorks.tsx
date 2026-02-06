
export default function HowItWorks() {
    const steps = [
        {
            icon: "🎙️",
            title: "سجل شعورك",
            desc: "ارفع مقطعاً صوتياً (رسالة، ضحكة، أو نبض قلب) لنحلل تردداته."
        },
        {
            icon: "✨",
            title: "الرسم الذهبي",
            desc: "نحول الترددات إلى لوحة مطبوعة برقائق ذهبية فاخرة وفريدة."
        },
        {
            icon: "📱",
            title: "أعد إحياء اللحظة",
            desc: "بمجرد مسح اللوحة بالهاتف، سينطلق الصوت لتستعيد الذكرى فوراً."
        }
    ];

    return (
        <section id="how-it-works" className="bg-[#0d121b] rounded-[40px] my-10 py-16 text-center">
            <h2 className="gold-text text-3xl font-bold mb-12">كيف تعمل Rouisia Voice؟</h2>

            <div className="flex flex-wrap justify-center gap-10">
                {steps.map((step, idx) => (
                    <div key={idx} className="flex-1 min-w-[250px] max-w-[350px]">
                        <div className="w-[70px] h-[70px] bg-[linear-gradient(45deg,_#BF953F,_#FCF6BA,_#AA771C)] rounded-full flex items-center justify-center mx-auto mb-6 text-3xl text-black shadow-lg">
                            {step.icon}
                        </div>
                        <h3 className="text-2xl font-bold mb-3 font-serif">{step.title}</h3>
                        <p className="text-gray-400 leading-relaxed">{step.desc}</p>
                    </div>
                ))}
            </div>
        </section>
    );
}
