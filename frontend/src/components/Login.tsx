"use client";

import { useState } from "react";
import { Lock } from "lucide-react";
import { loginUser } from "@/lib/api";

interface LoginProps {
    onLogin: () => void;
}

export default function Login({ onLogin }: LoginProps) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setLoading(true);
        try {
            const response = await loginUser({ email, password });
            if (response.success) {
                localStorage.setItem("admin_authenticated", "true");
                localStorage.setItem("admin_role", response.role);
                localStorage.setItem("admin_agent_name", response.agent_name || "");
                onLogin();
            } else {
                setError("البريد الإلكتروني أو كلمة المرور غير صحيحة");
            }
        } catch (err: any) {
            setError(err.response?.data?.error || "حدث خطأ أثناء تسجيل الدخول أو بيانات غير صحيحة");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-[#0B0F17] flex items-center justify-center p-4 font-cairo">
            <div className="bg-[#121926]/90 border border-[#D4AF37]/20 backdrop-blur-md p-8 rounded-3xl shadow-2xl w-full max-w-md relative overflow-hidden">
                {/* Decorative gradients */}
                <div className="absolute -top-24 -left-24 w-48 h-48 bg-[#D4AF37]/10 rounded-full blur-3xl pointer-events-none" />
                <div className="absolute -bottom-24 -right-24 w-48 h-48 bg-blue-500/10 rounded-full blur-3xl pointer-events-none" />

                <div className="flex justify-center mb-6 relative">
                    <div className="w-20 h-20 bg-gradient-to-tr from-[#AA771C] via-[#FCF6BA] to-[#BF953F] rounded-2xl flex items-center justify-center text-[#111] shadow-xl shadow-amber-950/20">
                        <Lock size={36} />
                    </div>
                </div>

                <h2 className="text-2xl font-bold text-center text-white mb-2 tracking-wide font-amiri">رويسية فويس</h2>
                <p className="text-xs text-center text-stone-400 mb-8">لوحة التحكم للمسؤولين والوكلاء</p>

                <form onSubmit={handleSubmit} className="space-y-6 relative">
                    <div>
                        <label className="block text-xs font-semibold text-stone-300 mb-2">البريد الإلكتروني</label>
                        <input
                            type="email"
                            required
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full px-4 py-3 bg-[#172030] text-white border border-stone-800 rounded-xl focus:ring-1 focus:ring-[#D4AF37] focus:border-[#D4AF37] outline-none transition-all text-sm placeholder:text-stone-500"
                            placeholder="admin@gmail.com"
                            dir="ltr"
                        />
                    </div>

                    <div>
                        <label className="block text-xs font-semibold text-stone-300 mb-2">كلمة المرور</label>
                        <input
                            type="password"
                            required
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full px-4 py-3 bg-[#172030] text-white border border-stone-800 rounded-xl focus:ring-1 focus:ring-[#D4AF37] focus:border-[#D4AF37] outline-none transition-all text-sm placeholder:text-stone-500"
                            placeholder="••••••"
                            dir="ltr"
                        />
                    </div>

                    {error && (
                        <div className="bg-rose-500/10 border border-rose-500/20 text-rose-400 p-3.5 rounded-xl text-xs text-center">
                            {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full py-3.5 bg-gradient-to-r from-[#BF953F] to-[#AA771C] text-[#111] rounded-xl font-bold hover:brightness-110 active:scale-[0.98] transition-all shadow-lg shadow-amber-950/20 text-sm disabled:opacity-50"
                    >
                        {loading ? "جاري الدخول..." : "تسجيل الدخول"}
                    </button>
                </form>
            </div>
        </div>
    );
}
