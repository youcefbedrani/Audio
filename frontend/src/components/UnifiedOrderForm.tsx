"use client";

import { useState } from "react";
import Image from "next/image";
import { Check, Loader2 } from "lucide-react";
import AudioRecorder from "./AudioRecorder";
import { createOrder } from "../lib/api";
import type { AudioData } from "../lib/types";
import { trackEvent } from "./PixelTracker";

// Hardcoded frames to match the new design's "Simple", "VIP", "Handmade" concept
// mapped to the existing backend logic if possible, or just using the IDs.
// The new HTML has:
// 1. Simple Order -> /assets/order-simple.png
// 2. VIP Order -> /assets/order-vip.png
// 3. Handmade Order -> /assets/order-handmade.png
const FRAMES = [
    {
        id: 1,
        title: "Simple Order",
        subtitle: "إطار عصري أنيق",
        price: 5000,
        image: "/assets/order-simple.png",
    },
    {
        id: 2,
        title: "VIP Order",
        subtitle: "إطار فاخر + تغليف ملكي",
        price: 6000,
        image: "/assets/order-vip.png",
    },
    {
        id: 3,
        title: "Handmade Order",
        subtitle: "إطار وتغليف مرصع مشغول يدوياً",
        price: 7000,
        image: "/assets/order-handmade.png",
    }
];

export default function UnifiedOrderForm() {
    const [selectedFrame, setSelectedFrame] = useState<number | null>(null);
    const [audioData, setAudioData] = useState<AudioData | null>(null);
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);
    const [scanId, setScanId] = useState<string | null>(null);

    const [formData, setFormData] = useState({
        name: "",
        phone: "",
        address: "" // acts as full address including wilaya
    });

    const handleAudioReady = (data: AudioData) => {
        setAudioData(data);
    };

    const handleSubmit = async () => {
        if (!selectedFrame || !audioData || !formData.name || !formData.phone || !formData.address) {
            alert("يرجى ملء جميع الحقول واختيار الإطار وتسجيل الصوت.");
            return;
        }

        setLoading(true);
        try {
            const frameEntry = FRAMES.find(f => f.id === selectedFrame);
            const price = frameEntry ? frameEntry.price : 3500;

            const response = await createOrder({
                id: 0, // Placeholder
                customer_name: formData.name,
                customer_phone: formData.phone,
                wilaya: "Other", // Defaulting to Other since we use single input
                delivery_address: formData.address,
                frame_id: selectedFrame,
                total_amount: price + 500, // + Delivery
                status: "pending"
            }, audioData.blob);

            if (response.success) {
                setSuccess(true);
                setScanId(response.order_id || "UNKNOWN");

                trackEvent("Purchase", {
                    value: price + 500,
                    currency: "DZD",
                    content_name: "Audio Frame Art",
                    content_category: "Gift",
                    content_ids: [selectedFrame]
                }, {
                    name: formData.name,
                    phone: formData.phone,
                    wilaya: "Other",
                    address: formData.address
                });

                window.scrollTo({ top: 0, behavior: "smooth" });
            }
        } catch (error) {
            console.error(error);
            alert("حدث خطأ أثناء إرسال الطلب. يرجى المحاولة مرة أخرى.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <section id="customization-section" className="py-12">
            <div className="bg-white text-[#111] p-8 md:p-12 rounded-[35px] max-w-[900px] mx-auto shadow-[0_30px_60px_rgba(0,0,0,0.5)] text-right">
                <h2 className="text-3xl font-bold text-center mb-8 font-serif">صمم تحفتك الخاصة</h2>

                {/* 1. Frame Selection */}
                <span className="block font-extrabold border-r-[5px] border-[#D4AF37] pr-4 mb-4 mt-8 text-xl">
                    1. اختر نوع الاطار والتغليف
                </span>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
                    {FRAMES.map((frame) => (
                        <div
                            key={frame.id}
                            onClick={() => setSelectedFrame(frame.id)}
                            className={`border-2 rounded-[20px] p-4 cursor-pointer text-center transition-all bg-white relative
                                ${selectedFrame === frame.id
                                    ? "border-[#D4AF37] bg-[#fffdf5] shadow-[0_10px_20px_rgba(212,175,55,0.1)]"
                                    : "border-[#eee]"
                                }`
                            }
                        >
                            <div className="relative w-full aspect-square mb-3 rounded-xl overflow-hidden">
                                <Image src={frame.image} alt={frame.title} fill className="object-contain" />
                            </div>
                            <strong className="block text-lg">{frame.title}</strong>
                            <p className="text-xs text-gray-500 mt-1">{frame.subtitle}</p>
                            <p className="font-bold text-[#D4AF37] mt-2">{frame.price} د.ج</p>
                            {selectedFrame === frame.id && (
                                <div className="absolute top-3 right-3 bg-[#D4AF37] text-black w-6 h-6 rounded-full flex items-center justify-center">
                                    <Check size={14} />
                                </div>
                            )}
                        </div>
                    ))}
                </div>

                {/* 2. Audio Recording */}
                <span className="block font-extrabold border-r-[5px] border-[#D4AF37] pr-4 mb-4 mt-10 text-xl">
                    2. ارفع البصمة الصوتية
                </span>

                <div className="bg-[#fffcf5] border-2 border-dashed border-[#D4AF37] p-6 rounded-[20px] text-center">
                    <AudioRecorder onAudioReady={handleAudioReady} />
                    <p className="text-sm text-gray-500 mt-2">(سيتم تحويل الصوت إلى موجات ذهبية)</p>
                </div>


                {/* 3. Shipping Info */}
                <span className="block font-extrabold border-r-[5px] border-[#D4AF37] pr-4 mb-4 mt-10 text-xl">
                    3. معلومات الشحن
                </span>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <input
                        type="text"
                        placeholder="الاسم الكامل"
                        className="w-full p-4 rounded-xl border border-[#ddd] focus:border-[#D4AF37] focus:outline-none"
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    />
                    <input
                        type="tel"
                        placeholder="رقم الهاتف"
                        className="w-full p-4 rounded-xl border border-[#ddd] focus:border-[#D4AF37] focus:outline-none text-right"
                        dir="ltr"
                        value={formData.phone}
                        onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    />
                </div>

                <div className="mt-4">
                    <input
                        type="text"
                        placeholder="العنوان الكامل (الولاية، البلدية، الحي...)"
                        className="w-full p-4 rounded-xl border border-[#ddd] focus:border-[#D4AF37] focus:outline-none"
                        value={formData.address}
                        onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                    />
                </div>

                {/* Submit */}
                <button
                    onClick={handleSubmit}
                    disabled={loading}
                    className="w-full mt-8 bg-[linear-gradient(45deg,_#BF953F,_#FCF6BA,_#AA771C)] text-black p-5 rounded-2xl text-xl font-extrabold shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-1 disabled:opacity-70 flex items-center justify-center gap-3"
                >
                    {loading ? (
                        <>
                            <Loader2 className="animate-spin" />
                            جاري الطلب...
                        </>
                    ) : (
                        "تأكيد الطلب الآن"
                    )}
                </button>
            </div>

            {/* Success Modal */}
            {success && (
                <div className="fixed inset-0 bg-[#111]/80 backdrop-blur-sm flex items-center justify-center z-[100] p-4">
                    <div className="bg-white rounded-[30px] p-10 text-center shadow-2xl max-w-lg w-full">
                        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6 text-green-600">
                            <Check size={40} />
                        </div>
                        <h2 className="text-2xl font-bold mb-4 text-[#111]">تم إرسال طلبك بنجاح!</h2>
                        <p className="text-gray-600 mb-8 leading-relaxed">
                            شكراً لثقتك بنا. يرجى انتظار اتصالنا لتأكيد الطلب والتوصيل.
                        </p>
                        {scanId && (
                            <div className="bg-gray-50 p-4 rounded-xl mb-8">
                                <p className="text-gray-500 text-[10px] uppercase tracking-widest mb-1">رقم الطلب</p>
                                <p className="font-mono text-xl font-bold text-[#111]">{scanId}</p>
                            </div>
                        )}
                        <button
                            onClick={() => window.location.reload()}
                            className="w-full py-4 bg-[#111] text-white rounded-2xl font-bold"
                        >
                            حسناً
                        </button>
                    </div>
                </div>
            )}
        </section>
    );
}
