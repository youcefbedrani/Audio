"use client";

import { useState } from "react";
import Image from "next/image";
import { Check, Mic, Truck, Loader2 } from "lucide-react";
import AudioRecorder from "./AudioRecorder";
import { createOrder } from "../lib/api";
import type { AudioData } from "../lib/types";
import { trackEvent } from "./PixelTracker";

// Hardcoded frames for simplicity, matching the API/landing page
const FRAMES = [
    {
        id: 1,
        title: "الإطار الكلاسيكي الأسود",
        price: 3500,
        image: "/frame-black.jpg", // Placeholder
        color: "bg-stone-900"
    },
    {
        id: 2,
        title: "الإطار الخشبي الطبيعي",
        price: 3500, // Normalized price
        image: "/frame-wood.jpg", // Placeholder
        color: "bg-[#8B4513]"
    },
    {
        id: 3,
        title: "الإطار الأبيض المودرن",
        price: 3500,
        image: "/frame-white.jpg", // Placeholder
        color: "bg-stone-100 border border-stone-200"
    }
];

export default function OrderSection() {
    const [step, setStep] = useState<1 | 2 | 3>(1);
    const [selectedFrame, setSelectedFrame] = useState<number | null>(null);
    const [audioData, setAudioData] = useState<AudioData | null>(null);
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);
    const [scanId, setScanId] = useState<string | null>(null);

    const [formData, setFormData] = useState({
        name: "",
        phone: "",
        wilaya: "",
        address: ""
    });

    const handleAudioReady = (data: AudioData) => {
        setAudioData(data);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!selectedFrame || !audioData) return;

        setLoading(true);
        try {
            const response = await createOrder({
                id: 0, // Placeholder
                customer_name: formData.name,
                customer_phone: formData.phone,
                wilaya: formData.wilaya,
                delivery_address: formData.address,
                frame_id: selectedFrame,
                total_amount: 4000, // 3500 (frame) + 500 (delivery)
                status: "pending"
            }, audioData.blob);

            if (response.success) {
                setSuccess(true);
                setScanId(response.order_id || "UNKNOWN");

                // Track Purchase
                trackEvent("Purchase", {
                    value: 4000,
                    currency: "DZD",
                    content_name: "Audio Frame Art",
                    content_category: "Gift",
                    content_ids: [selectedFrame]
                });

                // Scroll to top of success message
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
        <>
            <div id="order-form" className="max-w-4xl mx-auto bg-white rounded-[2.5rem] shadow-2xl overflow-hidden border border-stone-100">
                {/* Steps Header */}
                <div className="bg-stone-900 text-white p-6 flex justify-between items-center text-sm md:text-base">
                    <div className={`flex items-center gap-2 ${step >= 1 ? "text-white" : "text-stone-500"}`}>
                        <div className="w-8 h-8 rounded-full bg-stone-800 flex items-center justify-center border border-stone-700">1</div>
                        <span>اختر الإطار</span>
                    </div>
                    <div className="w-12 h-px bg-stone-700"></div>
                    <div className={`flex items-center gap-2 ${step >= 2 ? "text-white" : "text-stone-500"}`}>
                        <div className="w-8 h-8 rounded-full bg-stone-800 flex items-center justify-center border border-stone-700">2</div>
                        <span>سجل الصوت</span>
                    </div>
                    <div className="w-12 h-px bg-stone-700"></div>
                    <div className={`flex items-center gap-2 ${step >= 3 ? "text-white" : "text-stone-500"}`}>
                        <div className="w-8 h-8 rounded-full bg-stone-800 flex items-center justify-center border border-stone-700">3</div>
                        <span>العنوان</span>
                    </div>
                </div>

                <div className="p-8 md:p-12">
                    {/* Step 1: Select Frame */}
                    {step === 1 && (
                        <div className="space-y-8 animate-in slide-in-from-right duration-300">
                            <div className="text-center">
                                <h3 className="text-2xl font-bold mb-2">اختر الإطار المناسب</h3>
                                <p className="text-stone-500">جميع الإطارات بسعر موحد: <span className="font-bold text-stone-900">3500 د.ج</span></p>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                {FRAMES.map((frame) => (
                                    <div
                                        key={frame.id}
                                        onClick={() => setSelectedFrame(frame.id)}
                                        className={`
                        cursor-pointer rounded-2xl border-2 p-4 transition-all duration-200
                        ${selectedFrame === frame.id ? "border-stone-900 bg-stone-50 shadow-lg scale-105" : "border-stone-100 hover:border-stone-300"}
                      `}
                                    >
                                        <div className={`aspect-square w-full rounded-xl mb-4 ${frame.color} flex items-center justify-center`}>
                                            {/* Placeholder for real images */}
                                            <span className="text-stone-400 text-xs">Image Placeholder</span>
                                        </div>
                                        <h4 className="font-bold text-lg mb-1">{frame.title}</h4>
                                        <div className="flex justify-between items-center">
                                            <span className="text-stone-500 text-sm">30x40 cm</span>
                                            {selectedFrame === frame.id && <div className="w-6 h-6 bg-stone-900 rounded-full flex items-center justify-center text-white"><Check size={14} /></div>}
                                        </div>
                                    </div>
                                ))}
                            </div>

                            <div className="flex justify-end pt-4">
                                <button
                                    onClick={() => setStep(2)}
                                    disabled={!selectedFrame}
                                    className="px-8 py-3 bg-stone-900 text-white rounded-xl font-bold hover:bg-stone-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2"
                                >
                                    التالي: تسجيل الصوت
                                    <Mic size={18} />
                                </button>
                            </div>
                        </div>
                    )}

                    {/* Step 2: Audio */}
                    {step === 2 && (
                        <div className="space-y-8 animate-in slide-in-from-right duration-300">
                            <div className="text-center">
                                <h3 className="text-2xl font-bold mb-2">سجل رسالتك الخالدة</h3>
                                <p className="text-stone-500">يمكنك التسجيل مباشرة أو رفع ملف صوتي جاهز</p>
                            </div>

                            <AudioRecorder onAudioReady={handleAudioReady} />

                            <div className="flex justify-between pt-8">
                                <button
                                    onClick={() => setStep(1)}
                                    className="text-stone-500 hover:text-stone-900 font-medium"
                                >
                                    عودة
                                </button>
                                <button
                                    onClick={() => {
                                        setStep(3);
                                        trackEvent("InitiateCheckout");
                                    }}
                                    disabled={!audioData}
                                    className="px-8 py-3 bg-stone-900 text-white rounded-xl font-bold hover:bg-stone-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2"
                                >
                                    التالي: معلومات التوصيل
                                    <Truck size={18} />
                                </button>
                            </div>
                        </div>
                    )}

                    {/* Step 3: Checkout Form */}
                    {step === 3 && (
                        <form onSubmit={handleSubmit} className="space-y-6 animate-in slide-in-from-right duration-300">
                            <div className="text-center mb-8">
                                <h3 className="text-2xl font-bold mb-2">أين نرسل الهدية؟</h3>
                                <p className="text-stone-500">الدفع عند الاستلام بعد معاينة المنتج</p>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <label className="text-sm font-bold text-stone-700">الاسم الكامل</label>
                                    <input
                                        required
                                        type="text"
                                        value={formData.name}
                                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                        className="w-full p-3 rounded-xl border border-stone-200 focus:border-stone-900 focus:ring-1 focus:ring-stone-900 outline-none transition-all"
                                        placeholder="محمد بن عبد الله"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-sm font-bold text-stone-700">رقم الهاتف</label>
                                    <input
                                        required
                                        type="tel"
                                        dir="ltr"
                                        value={formData.phone}
                                        onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                                        className="w-full p-3 rounded-xl border border-stone-200 focus:border-stone-900 focus:ring-1 focus:ring-stone-900 outline-none transition-all text-right"
                                        placeholder="05 XX XX XX XX"
                                    />
                                </div>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <label className="text-sm font-bold text-stone-700">الولاية</label>
                                    <select
                                        required
                                        value={formData.wilaya}
                                        onChange={(e) => setFormData({ ...formData, wilaya: e.target.value })}
                                        className="w-full p-3 rounded-xl border border-stone-200 focus:border-stone-900 focus:ring-1 focus:ring-stone-900 outline-none transition-all bg-white"
                                    >
                                        <option value="">اختر الولاية</option>
                                        <option value="Adrar">01 أدرار</option>
                                        <option value="Chlef">02 الشلف</option>
                                        <option value="Laghouat">03 الأغواط</option>
                                        <option value="Oum El Bouaghi">04 أم البواقي</option>
                                        <option value="Batna">05 باتنة</option>
                                        <option value="Bejaia">06 بجاية</option>
                                        <option value="Biskra">07 بسكرة</option>
                                        <option value="Bechar">08 بشار</option>
                                        <option value="Blida">09 البليدة</option>
                                        <option value="Bouira">10 البويرة</option>
                                        <option value="Algiers">16 الجزائر العاصمة</option>
                                        <option value="Setif">19 سطيف</option>
                                        <option value="Oran">31 وهران</option>
                                        <option value="Constantine">25 قسنطينة</option>
                                        <option value="other">ولاية أخرى</option>
                                    </select>
                                </div>
                                <div className="space-y-2">
                                    <label className="text-sm font-bold text-stone-700">البلدية / العنوان</label>
                                    <input
                                        required
                                        type="text"
                                        value={formData.address}
                                        onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                                        className="w-full p-3 rounded-xl border border-stone-200 focus:border-stone-900 focus:ring-1 focus:ring-stone-900 outline-none transition-all"
                                        placeholder="حي الزهور، شارع 1..."
                                    />
                                </div>
                            </div>

                            <div className="bg-stone-50 p-6 rounded-xl mt-6 border border-stone-100">
                                <div className="flex justify-between items-center mb-2">
                                    <span className="text-stone-600">سعر الإطار</span>
                                    <span className="font-bold">3500 د.ج</span>
                                </div>
                                <div className="flex justify-between items-center mb-4">
                                    <span className="text-stone-600">التوصيل</span>
                                    <span className="font-bold">500 د.ج</span>
                                </div>
                                <div className="h-px bg-stone-200 my-4"></div>
                                <div className="flex justify-between items-center text-xl">
                                    <span className="font-bold text-stone-900">المجموع الكلي</span>
                                    <span className="font-bold text-stone-900">4000 د.ج</span>
                                </div>
                            </div>

                            <div className="flex justify-between items-center pt-4">
                                <button
                                    type="button"
                                    onClick={() => setStep(2)}
                                    className="text-stone-500 hover:text-stone-900 font-medium"
                                >
                                    عودة
                                </button>
                                <button
                                    type="submit"
                                    disabled={loading}
                                    className="flex-1 mr-4 py-4 bg-stone-900 text-white rounded-xl font-bold text-lg hover:bg-stone-800 disabled:opacity-70 transition-all shadow-lg hover:shadow-xl flex items-center justify-center gap-3"
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
                        </form>
                    )}
                </div>
            </div>

            {/* Success Popup Modal */}
            {success && (
                <div className="fixed inset-0 bg-stone-900/60 backdrop-blur-md flex items-center justify-center z-[100] p-4 animate-in fade-in duration-300">
                    <div className="bg-white rounded-3xl p-8 md:p-12 text-center shadow-2xl max-w-lg w-full border border-stone-100 animate-in zoom-in duration-500">
                        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6 text-green-600">
                            <Check size={40} />
                        </div>
                        <h2 className="text-2xl font-bold mb-4 text-stone-900">تم إرسال طلبك بنجاح!</h2>
                        <p className="text-stone-600 mb-8 text-lg leading-relaxed">
                            شكراً لثقتك بنا. يرجى انتظار اتصالنا لتأكيد الطلب والتوصيل.
                        </p>

                        {scanId && (
                            <div className="bg-stone-50 p-4 rounded-xl mb-8 border border-stone-100">
                                <p className="text-stone-500 text-[10px] uppercase tracking-widest mb-1">رقم الطلب</p>
                                <p className="font-mono text-xl font-bold text-stone-900">{scanId}</p>
                            </div>
                        )}

                        <button
                            onClick={() => window.location.reload()}
                            className="w-full py-4 bg-stone-900 text-white rounded-2xl font-bold hover:bg-black transition-all shadow-lg hover:shadow-black/20"
                        >
                            حسناً، فهمت
                        </button>
                    </div>
                </div>
            )}
        </>
    );
}
