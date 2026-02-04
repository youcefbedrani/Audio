"use client";

import { useState } from "react";
import { Lock } from "lucide-react";

interface LoginProps {
    onLogin: () => void;
}

export default function Login({ onLogin }: LoginProps) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (email === "admin@gmail.com" && password === "admin") {
            localStorage.setItem("admin_authenticated", "true");
            onLogin();
        } else {
            setError("البريد الإلكتروني أو كلمة المرور غير صحيحة");
        }
    };

    return (
        <div className="min-h-screen bg-stone-50 flex items-center justify-center p-4">
            <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md">
                <div className="flex justify-center mb-6">
                    <div className="w-16 h-16 bg-stone-900 rounded-full flex items-center justify-center text-white">
                        <Lock size={32} />
                    </div>
                </div>
                <h2 className="text-2xl font-bold text-center text-stone-900 mb-8">تسجيل الدخول للمسؤول</h2>

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium text-stone-700 mb-2">البريد الإلكتروني</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full p-3 border border-stone-200 rounded-xl focus:ring-2 focus:ring-stone-900 focus:border-stone-900 outline-none transition-all"
                            placeholder="admin@gmail.com"
                            dir="ltr"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-stone-700 mb-2">كلمة المرور</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full p-3 border border-stone-200 rounded-xl focus:ring-2 focus:ring-stone-900 focus:border-stone-900 outline-none transition-all"
                            placeholder="••••••"
                            dir="ltr"
                        />
                    </div>

                    {error && (
                        <div className="bg-red-50 text-red-600 p-3 rounded-lg text-sm text-center">
                            {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        className="w-full py-3 bg-stone-900 text-white rounded-xl font-bold hover:bg-stone-800 transition-colors shadow-lg"
                    >
                        دخول
                    </button>
                </form>
            </div>
        </div>
    );
}
