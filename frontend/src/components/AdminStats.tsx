import { Order } from "@/lib/types";
import { Package, CheckCircle, Truck, DollarSign } from "lucide-react";

interface AdminStatsProps {
    orders: Order[];
}

export default function AdminStats({ orders }: AdminStatsProps) {
    // Calculate statistics
    const totalOrders = orders.length;

    const confirmedOrders = orders.filter(o => o.status === 'confirmed').length;

    const shippedOrders = orders.filter(o => o.status === 'shipped');
    const shippedCount = shippedOrders.length;

    // Revenue from SHIPPED orders only
    const totalRevenue = shippedOrders.reduce((sum, order) => {
        return sum + (Number(order.total_amount) || 0);
    }, 0);

    const stats = [
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
            value: shippedCount,
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
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            {stats.map((stat, index) => (
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
    );
}
