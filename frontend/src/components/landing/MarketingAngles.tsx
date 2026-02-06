import Image from 'next/image';

const angles = [
    {
        title: "ضحكة أمي.. حياة",
        desc: "لأن ضحكتها هي أجمل نغمة في الكون، قمنا بتخليد تردداتها برقائق ذهبية فاخرة. عندما تشتاق لسماعها، فقط وجّه هاتفك نحو اللوحة لتمتلئ الغرفة ببهجتها الصادقة.",
        image: "/assets/story-mother.jpg",
        alt: "ضحكة أمي"
    },
    {
        title: "صوتٌ يطوي المسافات",
        desc: "لأن الغربة مُرة، وصوت من نحب هو الأمان.. وثّق رسالة من شخص بعيد أو ذكرى من غائب لا تغادر بالك. قطعة فنية تجعلك تشعر أنهم معك في نفس الغرفة، بلمسات ذهبية تليق بغلاوة أصحابها.",
        image: "/assets/story-distance.jpg",
        alt: "صوت يطوي المسافات",
        reversed: true
    },
    {
        title: "وعدٌ مخلد بالبريق",
        desc: "كلمة \"أحبك\" بلمعان ذهبي جذاب. حوّل وعودك لشريك حياتك إلى لوحة فاخرة تعانق جدران منزلكم، لتكون تذكيراً دائماً بأن صوت الحب لا ينتهي أبداً.",
        image: "/assets/story-love.jpg",
        alt: "رسالة حب ذهبية"
    }
];

export default function MarketingAngles() {
    return (
        <section className="space-y-0">
            {angles.map((angle, idx) => (
                <div key={idx} className={`flex flex-col ${angle.reversed ? 'md:flex-row-reverse' : 'md:flex-row'} items-center gap-12 py-20 border-t border-[rgba(212,175,55,0.15)] text-right`}>

                    <div className="flex-1">
                        <h2 className="text-4xl text-[#D4AF37] font-bold mb-6">{angle.title}</h2>
                        <p className="text-lg leading-8 opacity-80">{angle.desc}</p>
                    </div>

                    <div className="flex-1 w-full">
                        <div className="relative h-[350px] w-full rounded-[30px] overflow-hidden border border-[rgba(212,175,55,0.15)] shadow-[0_20px_40px_rgba(0,0,0,0.4)]">
                            <Image
                                src={angle.image}
                                alt={angle.alt}
                                fill
                                className="object-cover"
                            />
                        </div>
                    </div>

                </div>
            ))}
        </section>
    );
}
