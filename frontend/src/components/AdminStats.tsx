import { AdminStatsData } from "@/lib/types";
import { Package, CheckCircle, Truck, DollarSign, Users } from "lucide-react";

interface AdminStatsProps {
    stats: AdminStatsData | null;
    role?: string;
}

export default function AdminStats({ stats, role = "admin" }: AdminStatsProps) {
    const totalOrders = stats?.total_orders || 0;
    const confirmedOrders = stats?.confirmed_orders || 0;
    const shippedOrders = stats?.shipped_orders || 0;
    const totalRevenue = stats?.total_revenue || 0;
    const agentStats = stats?.agent_stats || {};

    const statsCards = [
        {
            title: "إجمالي الطلبات",
            value: totalOrders,
            icon: Package,
            color: "bg-blue-500/10 text-blue-400 border-blue-500/20",
        },
        {
            title: "الطلبات المؤكدة",
            value: confirmedOrders,
            icon: CheckCircle,
            color: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
        },
        {
            title: "الطلبات المشحونة",
            value: shippedOrders,
            icon: Truck,
            color: "bg-indigo-500/10 text-indigo-400 border-indigo-500/20",
        },
        {
            title: "عائد المبيعات (المشحون)",
            value: `${totalRevenue.toLocaleString()} د.ج`,
            icon: DollarSign,
            color: "bg-amber-500/10 text-[#D4AF37] border-amber-500/20",
        }
    ];

    return (
        <div className="font-cairo">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                {statsCards.map((stat, index) => (
                    <div
                        key={index}
                        className="bg-[#121926]/90 border border-[#D4AF37]/15 rounded-2xl p-6 shadow-xl relative overflow-hidden transition-all hover:translate-y-[-2px] hover:border-[#D4AF37]/30"
                    >
                        <div className="absolute -top-12 -left-12 w-24 h-24 bg-white/5 rounded-full blur-xl pointer-events-none" />
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-xs font-semibold text-stone-400 mb-2">{stat.title}</p>
                                <h3 className="text-2xl font-bold text-white font-sans">{stat.value}</h3>
                            </div>
                            <div className={`p-3.5 rounded-xl border ${stat.color} shadow-sm`}>
                                <stat.icon size={22} />
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Employee Statistics - Only visible to admin */}
            {role === "admin" && (
                <div className="bg-[#121926]/90 border border-[#D4AF37]/15 rounded-2xl p-6 shadow-xl mb-8 relative overflow-hidden">
                    <div className="absolute -top-12 -left-12 w-24 h-24 bg-white/5 rounded-full blur-xl pointer-events-none" />
                    <h3 className="text-md font-bold text-white mb-4 flex items-center gap-2 border-r-4 border-[#D4AF37] pr-2">
                        <Users className="w-5 h-5 text-[#D4AF37]" />
                        أداء فريق العمل (الطلبات المؤكدة)
                    </h3>
                    <div className="overflow-x-auto">
                        <table className="w-full text-right text-sm">
                            <thead className="bg-[#172030] text-stone-400 font-semibold border-b border-stone-800">
                                <tr>
                                    <th className="py-3 px-4 rounded-r-xl">الموظف</th>
                                    <th className="py-3 px-4">عدد الطلبات المؤكدة</th>
                                    <th className="py-3 px-4 rounded-l-xl">نسبة الأداء</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-stone-800/50">
                                {Object.entries(agentStats)
                                    .sort(([, a], [, b]) => b - a)
                                    .map(([agent, count]) => (
                                        <tr key={agent} className="hover:bg-[#172030]/50 transition-colors">
                                            <td className="py-3.5 px-4 font-medium text-stone-200">{agent}</td>
                                            <td className="py-3.5 px-4 text-emerald-400 font-bold">{count}</td>
                                            <td className="py-3.5 px-4 text-stone-400 font-sans">
                                                {Math.round((count / (confirmedOrders || 1)) * 100)}%
                                            </td>
                                        </tr>
                                    ))}
                                {Object.keys(agentStats).length === 0 && (
                                    <tr>
                                        <td colSpan={3} className="py-8 text-center text-stone-500 italic">لا توجد بيانات أداء متاحة حالياً</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    );
}
