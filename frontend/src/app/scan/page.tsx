"use client";

import { useState, useRef } from "react";
import WebScanner from "@/components/WebScanner";
import Link from "next/link";
import { ArrowRight, Play, Pause, Music, User, Clock, Loader2, Volume2, AlertCircle, Camera, Keyboard } from "lucide-react";
import axios from "axios";

export default function ScanPage() {
    const [mode, setMode] = useState<"choice" | "camera" | "manual">("choice");
    const [idInput, setIdInput] = useState("");
    const [orderData, setOrderData] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const audioRef = useRef<HTMLAudioElement | null>(null);

    // Dynamic API URL detection
    const getBaseUrl = () => {
        if (typeof window === 'undefined') return "";
        const host = window.location.hostname;
        const protocol = window.location.protocol;
        return `${protocol}//${host}`;
    };
    const BASE_URL = getBaseUrl();

    function cleanId(value: string): string {
        return value
            .replace(/[^A-Za-z0-9]/g, "")
            .toUpperCase()
            .trim();
    }

    const handleScan = async (rawValue: string) => {
        console.log("Scanned raw:", rawValue);
        const id = cleanId(rawValue);
        console.log("Cleaned ID:", id);

        if (!id) return;

        await lookupAudio(id);
    };

    const handleManualLookup = async (e: React.FormEvent) => {
        e.preventDefault();
        const id = cleanId(idInput);

        if (!id) {
            setError("Please enter a valid ID");
            return;
        }

        await lookupAudio(id);
    };

    const lookupAudio = async (id: string) => {
        setIsLoading(true);
        setError(null);
        setOrderData(null);

        try {
            console.log("Looking up ID:", id);
            const response = await axios.get(`${BASE_URL}/api/audio/${id}/`);

            if (response.data.success || response.data.audio_url) {
                setOrderData(response.data);

                // Auto-play audio immediately
                if (response.data.audio_url) {
                    const audioUrl = response.data.audio_url;

                    // Create minimal audio instance for immediate feedback
                    const audio = new Audio(audioUrl);

                    try {
                        // User interaction (camera click/tap) usually allows this
                        await audio.play();
                        setIsPlaying(true);
                    } catch (e) {
                        console.warn("Auto-play blocked by browser policy:", e);
                        // We still set isPlaying to true so the UI reflects it, 
                        // and the user can click play if needed.
                        setIsPlaying(false);
                    }

                    // Sync with the hidden audio element for persistence/controls
                    if (audioRef.current) {
                        audioRef.current.src = audioUrl;
                        // If the first one failed, this might too, but we try anyway
                        audioRef.current.play().catch(e => console.warn("Ref auto-play failed:", e));
                    }
                }
            } else {
                setError("No audio found for this ID");
            }
        } catch (err: any) {
            console.error("Audio lookup failed:", err);
            if (err.response?.status === 404) {
                setError("ID not found. Please check and try again.");
            } else {
                setError("Failed to lookup audio. Please try again.");
            }
        } finally {
            setIsLoading(false);
        }
    };

    const togglePlay = () => {
        if (audioRef.current) {
            if (isPlaying) {
                audioRef.current.pause();
            } else {
                audioRef.current.play();
            }
            setIsPlaying(!isPlaying);
        }
    };

    const resetLookup = () => {
        setMode("choice");
        setIdInput("");
        setOrderData(null);
        setError(null);
        setIsPlaying(false);
        if (audioRef.current) {
            audioRef.current.pause();
            audioRef.current.src = "";
        }
    };

    return (
        <div className="min-h-screen bg-stone-50 flex flex-col font-sans" dir="rtl">
            <header className="p-4 bg-white border-b border-stone-100 sticky top-0 z-10">
                <div className="container mx-auto flex items-center justify-between">
                    <Link href="/" className="flex items-center gap-2 text-stone-600 hover:text-stone-900 font-bold transition-colors">
                        <ArrowRight size={20} />
                        <span className="font-arabic">العودة للرئيسية</span>
                    </Link>
                    <h1 className="text-lg md:text-xl font-bold text-stone-900 font-arabic">البحث عن الإطار</h1>
                </div>
            </header>

            <div className="flex-1 flex flex-col items-center justify-center p-4">
                {!orderData ? (
                    <>
                        {mode === "choice" && (
                            <div className="w-full max-w-md space-y-4">
                                <div className="bg-white p-8 rounded-2xl shadow-xl border border-stone-100 text-center">
                                    <div className="w-16 h-16 bg-stone-900 rounded-full flex items-center justify-center mx-auto mb-4">
                                        <Music className="w-8 h-8 text-white" />
                                    </div>
                                    <h2 className="text-2xl font-bold text-stone-900 mb-2 font-arabic">كيف تريد البحث؟</h2>
                                    <p className="text-stone-500 text-sm font-arabic mb-6">اختر طريقة البحث عن الإطار</p>
                                </div>

                                <button
                                    onClick={() => setMode("camera")}
                                    className="w-full p-6 bg-white rounded-2xl shadow-lg border-2 border-stone-200 hover:border-stone-900 transition-all flex items-center gap-4"
                                >
                                    <div className="w-12 h-12 bg-stone-900 rounded-full flex items-center justify-center">
                                        <Camera className="w-6 h-6 text-white" />
                                    </div>
                                    <div className="text-right flex-1">
                                        <h3 className="font-bold text-lg text-stone-900 font-arabic">مسح الموجة الصوتية</h3>
                                        <p className="text-sm text-stone-500 font-arabic">استخدم الكاميرا لمسح الموجة الصوتية</p>
                                    </div>
                                </button>

                                <button
                                    onClick={() => setMode("manual")}
                                    className="w-full p-6 bg-white rounded-2xl shadow-lg border-2 border-stone-200 hover:border-stone-900 transition-all flex items-center gap-4"
                                >
                                    <div className="w-12 h-12 bg-stone-900 rounded-full flex items-center justify-center">
                                        <Keyboard className="w-6 h-6 text-white" />
                                    </div>
                                    <div className="text-right flex-1">
                                        <h3 className="font-bold text-lg text-stone-900 font-arabic">إدخال الرقم يدوياً</h3>
                                        <p className="text-sm text-stone-500 font-arabic">اكتب رقم الإطار مباشرة</p>
                                    </div>
                                </button>
                            </div>
                        )}

                        {mode === "camera" && (
                            <div className="w-full max-w-md">
                                <div className="bg-white p-3 rounded-2xl shadow-sm border border-stone-100 mb-6 text-center">
                                    <p className="text-stone-600 font-bold font-arabic">وجه الكاميرا نحو الإطار</p>
                                    <p className="text-stone-400 text-xs mt-1 font-arabic">سيتم التعرف على الموجة الصوتية وتشغيلها تلقائياً</p>
                                </div>
                                <WebScanner
                                    onScan={handleScan}
                                    onClose={() => setMode("choice")}
                                />
                            </div>
                        )}

                        {mode === "manual" && (
                            <div className="w-full max-w-md">
                                <div className="bg-white p-8 rounded-2xl shadow-xl border border-stone-100">
                                    <button
                                        onClick={() => setMode("choice")}
                                        className="mb-4 text-stone-600 hover:text-stone-900 flex items-center gap-2 font-arabic"
                                    >
                                        <ArrowRight size={16} />
                                        العودة
                                    </button>

                                    <div className="text-center mb-6">
                                        <div className="w-16 h-16 bg-stone-900 rounded-full flex items-center justify-center mx-auto mb-4">
                                            <Music className="w-8 h-8 text-white" />
                                        </div>
                                        <h2 className="text-2xl font-bold text-stone-900 mb-2 font-arabic">أدخل رقم الإطار</h2>
                                        <p className="text-stone-500 text-sm font-arabic">الرقم موجود أسفل الموجة الصوتية</p>
                                    </div>

                                    <form onSubmit={handleManualLookup} className="space-y-4">
                                        <div>
                                            <label className="block text-sm font-bold text-stone-700 mb-2 font-arabic">رقم الإطار</label>
                                            <input
                                                type="text"
                                                value={idInput}
                                                onChange={(e) => setIdInput(e.target.value)}
                                                placeholder="44AF3416AEC04ED"
                                                className="w-full p-4 border-2 border-stone-200 rounded-xl focus:ring-2 focus:ring-stone-900 focus:border-stone-900 outline-none transition-all font-mono text-center text-lg uppercase"
                                                dir="ltr"
                                                disabled={isLoading}
                                            />
                                        </div>

                                        {error && (
                                            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm font-arabic">
                                                {error}
                                            </div>
                                        )}

                                        <button
                                            type="submit"
                                            disabled={isLoading || !idInput.trim()}
                                            className="w-full py-4 bg-stone-900 text-white rounded-xl font-bold hover:bg-stone-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl flex items-center justify-center gap-2 font-arabic"
                                        >
                                            {isLoading ? (
                                                <>
                                                    <Loader2 className="w-5 h-5 animate-spin" />
                                                    جاري البحث...
                                                </>
                                            ) : (
                                                <>
                                                    <Play className="w-5 h-5" />
                                                    تشغيل الصوت
                                                </>
                                            )}
                                        </button>
                                    </form>
                                </div>
                            </div>
                        )}
                    </>
                ) : (
                    <div className="w-full max-w-md animate-in fade-in zoom-in duration-500">
                        <div className="space-y-6">
                            {/* Success Header */}
                            <div className="bg-white p-8 rounded-3xl shadow-xl border border-stone-100 text-center relative overflow-hidden">
                                <div className="absolute top-0 right-0 w-32 h-32 bg-blue-50 rounded-bl-full -mr-16 -mt-16 opacity-50"></div>

                                <div className="w-20 h-20 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-6 relative">
                                    <Music className="w-10 h-10" />
                                    <div className="absolute -bottom-1 -left-1 w-6 h-6 bg-white rounded-full flex items-center justify-center shadow-sm">
                                        <div className="w-4 h-4 bg-green-500 rounded-full"></div>
                                    </div>
                                </div>

                                <h3 className="font-bold text-2xl text-stone-900 mb-2 font-arabic">تم العثور على الإطار!</h3>
                                <p className="text-stone-500 mb-8 font-arabic">{orderData.frame_title || "إطار صوتي خاص"}</p>

                                {/* Audio Player Card */}
                                <div className="bg-stone-900 rounded-2xl p-6 mb-8 text-white shadow-2xl relative">
                                    <div className="flex items-center justify-between mb-6">
                                        <div className="flex items-center gap-3">
                                            <div className="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center">
                                                <Volume2 className="w-5 h-5 text-blue-400" />
                                            </div>
                                            <div className="text-right">
                                                <p className="text-[10px] text-stone-400 uppercase font-bold tracking-widest font-arabic">صوت الإطار</p>
                                                <p className="font-bold text-sm truncate max-w-[150px] font-arabic">{orderData.order?.customer_name || "عميل مميز"}</p>
                                            </div>
                                        </div>
                                        <button
                                            onClick={togglePlay}
                                            className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center hover:bg-blue-500 transition-all active:scale-95 shadow-lg shadow-blue-900/40"
                                        >
                                            {isPlaying ? <Pause className="w-8 h-8 fill-white" /> : <Play className="w-8 h-8 fill-white ml-1" />}
                                        </button>
                                    </div>

                                    {/* Simple Waveform Placeholder */}
                                    <div className="flex items-end justify-between h-8 gap-1 px-2">
                                        {[...Array(20)].map((_, i) => (
                                            <div
                                                key={i}
                                                className={`w-full bg-blue-500/30 rounded-full transition-all duration-300 ${isPlaying ? 'animate-pulse' : ''}`}
                                                style={{ height: `${20 + Math.random() * 80}%`, animationDelay: `${i * 0.1}s` }}
                                            ></div>
                                        ))}
                                    </div>

                                    <audio
                                        ref={audioRef}
                                        src={orderData.audio_url}
                                        onPlay={() => setIsPlaying(true)}
                                        onPause={() => setIsPlaying(false)}
                                        onEnded={() => setIsPlaying(false)}
                                        className="hidden"
                                    />
                                </div>

                                {/* Order Metadata */}
                                <div className="grid grid-cols-2 gap-4 text-right mb-8">
                                    <div className="p-3 bg-stone-50 rounded-xl border border-stone-100">
                                        <div className="flex items-center gap-2 mb-1 text-stone-400">
                                            <User size={14} />
                                            <span className="text-[10px] font-bold font-arabic">صاحب الإطار</span>
                                        </div>
                                        <p className="text-xs font-bold text-stone-700 font-arabic truncate">{orderData.order?.customer_name || "---"}</p>
                                    </div>
                                    <div className="p-3 bg-stone-50 rounded-xl border border-stone-100">
                                        <div className="flex items-center gap-2 mb-1 text-stone-400">
                                            <Clock size={14} />
                                            <span className="text-[10px] font-bold font-arabic">تاريخ الإنشاء</span>
                                        </div>
                                        <p className="text-xs font-bold text-stone-700 font-arabic">
                                            {orderData.order?.created_at ? new Date(orderData.order.created_at).toLocaleDateString('ar-DZ') : "---"}
                                        </p>
                                    </div>
                                </div>

                                <button
                                    onClick={resetLookup}
                                    className="w-full py-4 bg-stone-100 text-stone-600 rounded-2xl font-bold hover:bg-stone-200 transition-all flex items-center justify-center gap-2 font-arabic"
                                >
                                    <Music size={18} />
                                    البحث عن إطار آخر
                                </button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
