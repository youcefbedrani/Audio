import { AdminStatsData } from "@/lib/types";
import { Package, CheckCircle, Truck, DollarSign, Users } from "lucide-react";

interface AdminStatsProps {
    stats: AdminStatsData | null;
}

export default function AdminStats({ stats }: AdminStatsProps) {
    const totalOrders = stats?.total_orders || 0;
    const confirmedOrders = stats?.confirmed_orders || 0;
    const shippedOrders = stats?.shipped_orders || 0;
    const totalRevenue = stats?.total_revenue || 0;
    const agentStats = stats?.agent_stats || {};

    const statsCards = [
        {
            title: "Total Orders",
            value: totalOrders,
            icon: Package,
            color: "bg-blue-100 text-blue-600",
            borderColor: "border-blue-200"
        },
        {
            title: "Confirmed Orders",
            value: confirmedOrders,
            icon: CheckCircle,
            color: "bg-green-100 text-green-600",
            borderColor: "border-green-200"
        },
        {
            title: "Shipped Orders",
            value: shippedOrders,
            icon: Truck,
            color: "bg-purple-100 text-purple-600",
            borderColor: "border-purple-200"
        },
        {
            title: "Revenue (Shipped)",
            value: `${totalRevenue.toLocaleString()} DA`,
            icon: DollarSign,
            color: "bg-yellow-100 text-yellow-600",
            borderColor: "border-yellow-200"
        }
    ];

    return (
        <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                {statsCards.map((stat, index) => (
                    <div
                        key={index}
                        className={`bg-white p-6 rounded-xl border ${stat.borderColor} shadow-sm hover:shadow-md transition-shadow`}
                    >
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm font-medium text-gray-500 mb-1">{stat.title}</p>
                                <h3 className="text-2xl font-bold text-gray-900">{stat.value}</h3>
                            </div>
                            <div className={`p-3 rounded-full ${stat.color}`}>
                                <stat.icon size={24} />
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Employee Statistics */}
            <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6 mb-8">
                <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
                    <Users className="w-5 h-5 text-gray-500" />
                    أداء فريق العمل (الطلبات المؤكدة)
                </h3>
                <div className="overflow-x-auto">
                    <table className="w-full text-right">
                        <thead className="bg-gray-50 text-gray-600 text-sm font-semibold border-b border-gray-100">
                            <tr>
                                <th className="py-3 px-4">الموظف</th>
                                <th className="py-3 px-4">عدد الطلبات المؤكدة</th>
                                <th className="py-3 px-4">نسبة الأداء</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-100">
                            {Object.entries(agentStats)
                                .sort(([, a], [, b]) => b - a)
                                .map(([agent, count], index) => (
                                    <tr key={agent} className="hover:bg-gray-50 transition-colors">
                                        <td className="py-3 px-4 font-medium text-gray-900">{agent}</td>
                                        <td className="py-3 px-4 text-green-600 font-bold">{count}</td>
                                        <td className="py-3 px-4 text-gray-500">
                                            {Math.round((count / (confirmedOrders || 1)) * 100)}%
                                        </td>
                                    </tr>
                                ))}
                            {Object.keys(agentStats).length === 0 && (
                                <tr>
                                    <td colSpan={3} className="py-8 text-center text-gray-400">لا توجد بيانات متاحة حالياً</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </>
    );
}
