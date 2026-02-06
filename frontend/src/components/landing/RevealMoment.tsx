import Image from 'next/image';

export default function RevealMoment() {
    return (
        <section className="bg-[linear-gradient(180deg,_rgba(26,36,49,0)_0%,_#1a2431_100%)] rounded-[40px] px-8 py-16 -mt-12 relative z-10 mx-auto max-w-7xl">
            <div className="flex flex-col md:flex-row items-center justify-center gap-10 text-right">

                {/* Text Content */}
                <div className="flex-1 min-w-[300px] order-2 md:order-1">
                    <h2 className="gold-text text-4xl font-bold mb-6">أنت من يمنحها الحياة!</h2>
                    <p className="text-xl leading-8 text-gray-300">
                        السر ليس فقط في الجمال، بل في لحظة الكشف. صاحب الهدية هو من يقوم <strong className="text-white">بنزع الرقائق الذهبية</strong> الزائدة بيده ليكتشف بصمة صوته الفريدة المختبئة بالأسفل. تجربة شعورية لا تُنسى تجعل من الهدية ذكرى محفورة في القلب.
                    </p>
                </div>

                {/* Video/Image Placeholder */}
                <div className="flex-1 min-w-[300px] max-w-[500px] rounded-[20px] overflow-hidden shadow-[0_0_30px_var(--gold-main)] border-2 border-[var(--gold-main)] order-1 md:order-2">
                    <Image
                        src="/assets/reveal-moment.jpg"
                        alt="لحظة نزع الرقائق الذهبية"
                        width={500}
                        height={300}
                        className="w-full h-auto object-cover"
                    />
                </div>

            </div>
        </section>
    );
}
