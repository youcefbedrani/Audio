"use client";

import { useState, useEffect } from "react";
import { Search, Download, Play, Pause, ExternalLink, UserCheck, Plus, UserPlus, Trash2, Edit, ChevronLeft, ChevronRight, X, Save, Users, Copy, Settings as SettingsIcon } from "lucide-react";
import { getOrders, updateOrderStatus, getConfirmationAgents, addConfirmationAgent, deleteConfirmationAgent, deleteOrder, updateOrderDetails, getSettings, updateSettings, Settings } from "@/lib/api";
import { Order } from "@/lib/types";
import Login from "@/components/Login";



export default function AdminPage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [orders, setOrders] = useState<Order[]>([]);
  // In pagination mode, we might filter visible items or search via API. 
  // For simplicity with the provided backend update, we will filter visible items.
  const [visibleOrders, setVisibleOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [playingAudio, setPlayingAudio] = useState<string | null>(null);
  const [viewingImage, setViewingImage] = useState<string | null>(null);

  // Pagination
  const [page, setPage] = useState(1);
  const [limit] = useState(1000);
  const [totalPages, setTotalPages] = useState(1);
  const [totalOrders, setTotalOrders] = useState(0);

  // Edit Modal
  const [editingOrder, setEditingOrder] = useState<Order | null>(null);
  const [editForm, setEditForm] = useState<Partial<Order>>({});

  // Confirmation Agents
  const [agents, setAgents] = useState<string[]>([]);
  const [newAgentName, setNewAgentName] = useState("");

  // Pixel Settings
  const [pixelSettings, setPixelSettings] = useState<Settings>({ fb_pixel_id: "", tiktok_pixel_id: "" });
  const [isSavingSettings, setIsSavingSettings] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

  useEffect(() => {
    const savedAuth = localStorage.getItem("admin_authenticated");
    if (savedAuth === "true") {
      setIsAuthenticated(true);
    }
  }, []);



  const loadSettings = async () => {
    try {
      const data = await getSettings();
      setPixelSettings(data);
    } catch (error) {
      console.error("Failed to load settings", error);
    }
  };

  const handleSaveSettings = async () => {
    setIsSavingSettings(true);
    try {
      await updateSettings(pixelSettings);
      alert("تم حفظ الإعدادات بنجاح");
      setShowSettings(false);
    } catch (error) {
      alert("فشل حفظ الإعدادات");
    } finally {
      setIsSavingSettings(false);
    }
  };

  const fetchOrders = async (silent = false, signal?: AbortSignal) => {
    if (!silent) setLoading(true);
    try {
      console.log(`[Admin] Fetching orders (Page: ${page}, Limit: ${limit})...`);
      const data: any = await getOrders(page, limit, searchTerm);

      console.log(`[Admin] Orders received:`, data);

      if (data && data.orders) {
        setOrders(data.orders);
        setVisibleOrders(data.orders);
        setTotalPages(data.total_pages);
        setTotalOrders(data.total);
      } else {
        // Fallback for non-paginated response
        const ordersArr = Array.isArray(data) ? data : (data.results || []);
        console.log(`[Admin] Handled as array/results:`, ordersArr.length);

        // Only update if data changed to avoid flickering
        if (JSON.stringify(ordersArr) !== JSON.stringify(orders)) {
          setOrders(ordersArr);
          setVisibleOrders(ordersArr);
        }
      }
    } catch (error: any) {
      console.error("[Admin] Failed to load orders:", error);
      if (error.response) {
        console.error("[Admin] Server responded with:", error.response.status, error.response.data);
      } else if (error.request) {
        console.error("[Admin] No response received (Network Error)");
      } else {
        console.error("[Admin] Request setup error:", error.message);
      }
    } finally {
      if (!silent) setLoading(false);
    }
  };

  const loadAgents = async () => {
    try {
      const data = await getConfirmationAgents();
      setAgents(data || []);
    } catch (error) {
      console.error("Failed to load agents", error);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      loadAgents();
      loadSettings();

      // Initial Fetch with Debounce (for search/typing)
      const debounceTimer = setTimeout(() => {
        fetchOrders(false);
      }, 500);

      // Polling Interval - Increased to 30s to reduce load
      const interval = setInterval(() => {
        if (!document.hidden) {
          fetchOrders(true);
        }
      }, 30000);

      return () => {
        clearTimeout(debounceTimer);
        clearInterval(interval);
      };
    }
  }, [isAuthenticated, page, searchTerm]);

  const handleAddAgent = async () => {
    const trimmedName = newAgentName.trim();
    if (!trimmedName) return;

    // Optimistic Update
    const prevAgents = [...agents];
    setAgents([...agents, trimmedName]);
    setNewAgentName("");

    try {
      await addConfirmationAgent(trimmedName);
    } catch (error) {
      alert("فشل إضافة الاسم");
      setAgents(prevAgents); // Revert
    }
  };

  const handleDeleteAgent = async (name: string) => {
    if (!confirm(`هل أنت متأكد من حذف المكلف "${name}"؟`)) return;

    // Optimistic Update
    const prevAgents = [...agents];
    setAgents(agents.filter(a => a !== name));

    try {
      await deleteConfirmationAgent(name);
    } catch (error) {
      alert("فشل حذف المكلف");
      setAgents(prevAgents); // Revert
    }
  };

  const handleDeleteOrder = async (orderId: string | number) => {
    if (!confirm("هل أنت متأكد من حذف هذا الطلب؟")) return;
    try {
      await deleteOrder(orderId);
      // Optimistic delete
      const filterList = (list: Order[]) => list.filter((o) => o.id !== orderId);

      setOrders((prev) => filterList(prev));
      setVisibleOrders((prev) => filterList(prev));
      setTotalOrders((prev) => prev - 1);
    } catch (error) {
      alert("فشل حذف الطلب");
    }
  };

  const openEditModal = (order: Order) => {
    setEditingOrder(order);
    setEditForm({
      customer_name: order.customer_name,
      customer_phone: order.customer_phone,
      wilaya: order.wilaya,
      delivery_address: order.delivery_address,
      notes: order.notes,
      total_amount: order.total_amount,
    });
  };

  const handleSaveEdit = async () => {
    if (!editingOrder) return;
    try {
      await updateOrderDetails(editingOrder.id, editForm);
      // Optimistic update
      const updateList = (list: Order[]) =>
        list.map((o) =>
          o.id === editingOrder.id ? { ...o, ...editForm } : o
        );

      setOrders((prev) => updateList(prev));
      setVisibleOrders((prev) => updateList(prev));
      setEditingOrder(null);
    } catch (error) {
      alert("فشل حفظ التعديلات");
    }
  };

  const handleUpdateStatus = async (
    orderId: string | number,
    updates: { status?: string; confirmation_agent?: string }
  ) => {
    const currentOrder = orders.find((o) => o.id === orderId);
    if (!currentOrder) return;

    const newStatus = updates.status || currentOrder.status;
    const newAgent =
      updates.confirmation_agent !== undefined
        ? updates.confirmation_agent
        : currentOrder.confirmation_agent;

    try {
      // Optimistic update
      const updatedOrder = { ...currentOrder, status: newStatus as Order['status'], confirmation_agent: newAgent };

      const updateList = (list: Order[]) =>
        list.map((o) => (o.id === orderId ? updatedOrder : o));

      setOrders((prev) => updateList(prev));
      setVisibleOrders((prev) => updateList(prev));

      await updateOrderStatus(orderId, newStatus as string, newAgent);
    } catch (error) {
      console.error("Failed to update order", error);
      fetchOrders(); // Revert
      alert("حدث خطأ أثناء التحديث");
    }
  };

  const exportToCSV = () => {
    if (orders.length === 0) return;

    const headers = [
      "ID", "Scan ID", "Name", "Phone", "Wilaya", "Address", "Price", "Status", "Agent", "Date"
    ];

    const rows = visibleOrders.map((order) => [
      order.id,
      order.scan_id,
      `"${order.customer_name}"`,
      order.customer_phone,
      order.wilaya,
      `"${order.delivery_address}"`,
      order.total_amount,
      order.status,
      order.confirmation_agent || "",
      order.created_at ? new Date(order.created_at).toLocaleDateString() : "",
    ]);

    const csvContent = [
      headers.join(","),
      ...rows.map((row) => row.join(",")),
    ].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `orders_${new Date().toISOString().split("T")[0]}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const toggleAudio = (url: string) => {
    const audio = document.getElementById("audio-player") as HTMLAudioElement;
    if (playingAudio === url) {
      audio.pause();
      setPlayingAudio(null);
    } else {
      audio.src = url;
      audio.play();
      setPlayingAudio(url);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("admin_authenticated");
    setIsAuthenticated(false);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    // You could add a toast here
  };

  if (!isAuthenticated) {
    return <Login onLogin={() => setIsAuthenticated(true)} />;
  }

  return (
    <div className="min-h-screen bg-stone-50 p-6 md:p-12 font-sans" dir="rtl">
      <div className="max-w-7xl mx-auto">
        <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 gap-6">
          <div className="flex flex-col gap-4 w-full md:w-auto">
            <div className="flex gap-2 self-end">
              <button
                onClick={() => setShowSettings(!showSettings)}
                className="p-2.5 bg-white border border-stone-200 rounded-lg hover:bg-stone-50 transition-colors shadow-sm text-stone-700"
                title="إعدادات البيكسل"
              >
                <SettingsIcon size={20} />
              </button>
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-red-50 text-red-600 rounded-xl font-bold hover:bg-red-100 transition-colors text-sm"
              >
                تسجيل الخروج
              </button>
            </div>

            {showSettings && (
              <div className="bg-white p-4 rounded-2xl border border-stone-200 shadow-lg absolute top-40 right-6 z-40 w-80 animate-in fade-in slide-in-from-top-4">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="font-bold text-stone-900 border-r-4 border-stone-900 pr-2">إعدادات البيكسل</h3>
                  <button onClick={() => setShowSettings(false)} className="text-stone-400 hover:text-stone-900">
                    <X size={18} />
                  </button>
                </div>

                <div className="space-y-4">
                  <div>
                    <label className="block text-xs font-bold text-stone-600 mb-1">Facebook Pixel ID</label>
                    <input
                      type="text"
                      className="w-full p-2 border border-stone-200 rounded-lg text-sm outline-none focus:border-blue-500"
                      placeholder="Enter ID..."
                      value={pixelSettings.fb_pixel_id}
                      onChange={(e) => setPixelSettings({ ...pixelSettings, fb_pixel_id: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-stone-600 mb-1">TikTok Pixel ID</label>
                    <input
                      type="text"
                      className="w-full p-2 border border-stone-200 rounded-lg text-sm outline-none focus:border-red-500"
                      placeholder="Enter ID..."
                      value={pixelSettings.tiktok_pixel_id}
                      onChange={(e) => setPixelSettings({ ...pixelSettings, tiktok_pixel_id: e.target.value })}
                    />
                  </div>
                  <button
                    onClick={handleSaveSettings}
                    disabled={isSavingSettings}
                    className="w-full py-2 bg-stone-900 text-white rounded-lg font-bold hover:bg-black transition-colors flex items-center justify-center gap-2 text-sm disabled:opacity-50"
                  >
                    {isSavingSettings ? "جاري الحفظ..." : "حفظ الإعدادات"}
                  </button>
                </div>
              </div>
            )}

            {/* Confirmation Agents Management */}
            <div className="bg-white p-4 rounded-2xl border border-stone-100 shadow-sm">
              <div className="flex items-center gap-2 mb-3 text-stone-700 font-bold text-sm">
                <Users size={18} />
                <span>فريق العمل</span>
              </div>

              {/* Agent List Tags */}
              <div className="flex flex-wrap gap-2 mb-4 max-w-sm">
                {agents.map(agent => (
                  <div key={agent} className="flex items-center gap-1.5 px-2.5 py-1 bg-stone-100 text-stone-700 rounded-full text-xs font-medium group transition-all hover:bg-stone-200">
                    <span>{agent}</span>
                    <button
                      onClick={() => handleDeleteAgent(agent)}
                      className="text-stone-400 hover:text-red-500 transition-colors"
                      title="حذف"
                    >
                      <X size={12} />
                    </button>
                  </div>
                ))}
                {agents.length === 0 && <span className="text-xs text-stone-400 italic">لا يوجد مكلفين</span>}
              </div>

              {/* Add Agent Input */}
              <div className="flex gap-2">
                <div className="relative flex-1">
                  <UserPlus className="absolute right-3 top-2.5 text-stone-400" size={16} />
                  <input
                    type="text"
                    placeholder="إضافة مكلف جديد..."
                    className="w-full p-2 pr-10 rounded-lg border border-stone-200 outline-none focus:border-stone-900 text-sm"
                    value={newAgentName}
                    onChange={(e) => setNewAgentName(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleAddAgent()}
                  />
                </div>
                <button
                  onClick={handleAddAgent}
                  className="bg-stone-900 text-white px-3 rounded-lg hover:bg-black transition-colors"
                >
                  <Plus size={18} />
                </button>
              </div>
            </div>

            <div className="flex gap-2">
              <div className="relative flex-1 md:w-64">
                <Search className="absolute right-3 top-3 text-stone-400" size={18} />
                <input
                  type="text"
                  placeholder="بحث في الصفحة..."
                  className="w-full p-2.5 pr-10 rounded-lg border border-stone-200 outline-none focus:border-stone-900 text-sm"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>

              <button
                onClick={exportToCSV}
                className="bg-green-600 text-white px-4 py-2.5 rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2 shadow-sm font-bold text-sm"
              >
                <Download size={18} />
                <span className="hidden md:inline">CSV</span>
              </button>
            </div>
          </div>
        </header>

        {loading ? (
          <div className="text-center py-20 text-stone-500">جاري تحميل البيانات...</div>
        ) : (
          <div className="bg-white rounded-3xl shadow-sm border border-stone-100 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-right">
                <thead className="bg-stone-50 text-stone-600 font-bold border-b border-stone-100 text-sm">
                  <tr>
                    <th className="p-4">الطلب</th>
                    <th className="p-4">العميل</th>
                    <th className="p-4">تفاصيل</th>
                    <th className="p-4">السعر</th>
                    <th className="p-4">المكلف</th>
                    <th className="p-4">الحالة</th>
                    <th className="p-4">إجراءات</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-stone-100 text-sm">
                  {visibleOrders.map((order) => (
                    <tr key={order.id} className="hover:bg-stone-50/50 transition-colors">
                      <td className="p-4 align-top">
                        <div className="flex flex-col gap-1.5">
                          <div className="font-mono font-bold text-sm bg-stone-100 px-2 py-1 rounded w-fit flex items-center gap-2 group">
                            <span className="text-stone-900">#{order.scan_id || '---'}</span>
                            {order.scan_id && (
                              <button onClick={() => copyToClipboard(order.scan_id!)} className="text-stone-400 hover:text-stone-900 transition-colors" title="نسخ">
                                <Copy size={12} />
                              </button>
                            )}
                          </div>
                          <div className="text-[10px] text-stone-400 font-mono">الرقم الداخلي: {order.id}</div>
                        </div>
                        <div className="text-xs text-stone-500 mt-2 flex items-center gap-1">
                          <span>📅</span>
                          {order.created_at ? new Date(order.created_at).toLocaleDateString("en-GB") : "N/A"}
                        </div>
                        <div className="flex items-center gap-2 mt-3">
                          {order.audio_file_url ? (
                            <button
                              onClick={() => toggleAudio(order.audio_file_url!)}
                              className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-bold transition-all ${playingAudio === order.audio_file_url
                                ? "bg-stone-900 text-white shadow-lg scale-105"
                                : "bg-stone-100 hover:bg-stone-200 text-stone-700 border border-stone-200"
                                }`}
                              title={playingAudio === order.audio_file_url ? "إيقاف مؤقت" : "تشغيل الصوت"}
                            >
                              {playingAudio === order.audio_file_url ? <Pause size={14} /> : <Play size={14} />}
                              <span>{playingAudio === order.audio_file_url ? "توقف" : "استماع"}</span>
                            </button>
                          ) : (
                            <div className="text-[10px] text-stone-400 italic">لا يوجد تسجيل</div>
                          )}

                          {order.qr_code_url && (
                            <button
                              onClick={() => setViewingImage(order.qr_code_url!)}
                              className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-50 text-blue-700 border border-blue-100 hover:bg-blue-600 hover:text-white text-xs font-bold transition-all"
                              title="معاينة الموجة"
                            >
                              <ExternalLink size={14} />
                              <span>الموجة</span>
                            </button>
                          )}
                        </div>
                      </td>
                      <td className="p-4 align-top">
                        <div className="font-bold text-stone-900">{order.customer_name}</div>
                        <div className="text-stone-500" dir="ltr">
                          {order.customer_phone}
                        </div>
                      </td>
                      <td className="p-4 align-top">
                        <div className="text-stone-800">{order.wilaya}</div>
                        <div className="text-xs text-stone-500 max-w-[150px] truncate" title={order.delivery_address}>
                          {order.delivery_address}
                        </div>
                        <div className="text-xs text-stone-400 mt-1">{order.frame_title}</div>
                      </td>
                      <td className="p-4 align-top">
                        <div className="font-bold text-stone-900">{order.total_amount} د.ج</div>
                        <div className="text-xs text-stone-500 font-medium mt-1">
                          {order.frame_id === 1 ? "Simple" :
                            order.frame_id === 2 ? "VIP" :
                              order.frame_id === 3 ? "Handmade" :
                                order.frame_title || "Unknown"}
                        </div>
                      </td>
                      <td className="p-4 align-top">
                        <select
                          value={order.confirmation_agent || ""}
                          onChange={(e) =>
                            handleUpdateStatus(order.id, { confirmation_agent: e.target.value })
                          }
                          className="bg-stone-50 border border-stone-200 rounded px-2 py-1 text-xs w-28 cursor-pointer outline-none focus:border-stone-400"
                        >
                          <option value="">اختر...</option>
                          {agents.map((agent) => (
                            <option key={agent} value={agent}>
                              {agent}
                            </option>
                          ))}
                        </select>
                      </td>
                      <td className="p-4 align-top">
                        <select
                          value={order.status}
                          onChange={(e) => handleUpdateStatus(order.id, { status: e.target.value })}
                          className={`
                            px-2 py-1.5 rounded-lg text-xs font-bold border outline-none cursor-pointer w-28 text-center transition-all
                            ${order.status === "pending"
                              ? "bg-yellow-50 text-yellow-600 border-yellow-200"
                              : order.status === "confirmed"
                                ? "bg-green-50 text-green-600 border-green-200"
                                : order.status === "cancelled"
                                  ? "bg-red-50 text-red-600 border-red-200"
                                  : order.status === "no_response"
                                    ? "bg-orange-50 text-orange-600 border-orange-200"
                                    : order.status === "shipped"
                                      ? "bg-blue-50 text-blue-600 border-blue-200"
                                      : "bg-stone-50 text-stone-500 border-stone-100"
                            }
                          `}
                        >
                          <option value="pending">قيد الانتظار</option>
                          <option value="confirmed">تم التأكيد</option>
                          <option value="cancelled">ملغى</option>
                          <option value="no_response">لا يوجد رد</option>
                          <option value="shipped">تم الشحن</option>
                          <option value="delivered">تم التوصيل</option>
                        </select>
                      </td>
                      <td className="p-4 align-top">
                        <div className="flex gap-2">
                          <button
                            onClick={() => openEditModal(order)}
                            className="text-blue-600 hover:bg-blue-50 p-1.5 rounded transition-colors"
                            title="تعديل"
                          >
                            <Edit size={16} />
                          </button>
                          <button
                            onClick={() => handleDeleteOrder(order.id)}
                            className="text-red-600 hover:bg-red-50 p-1.5 rounded transition-colors"
                            title="حذف"
                          >
                            <Trash2 size={16} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {visibleOrders.length === 0 && (
                <div className="text-center py-20 text-stone-400">لا توجد طلبات</div>
              )}

              {/* Pagination Controls */}
              <div className="p-4 border-t border-stone-100 flex justify-between items-center bg-stone-50">
                <button
                  disabled={page <= 1}
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  className="flex items-center gap-1 px-3 py-1.5 rounded bg-white border border-stone-200 disabled:opacity-50 text-sm hover:bg-stone-100 transition-colors"
                >
                  <ChevronRight size={16} /> السابق
                </button>

                <span className="text-sm font-medium text-stone-600">
                  صفحة {page} من {totalPages}
                </span>

                <button
                  disabled={page >= totalPages}
                  onClick={() => setPage((p) => p + 1)}
                  className="flex items-center gap-1 px-3 py-1.5 rounded bg-white border border-stone-200 disabled:opacity-50 text-sm hover:bg-stone-100 transition-colors"
                >
                  التالي <ChevronLeft size={16} />
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Edit Modal */}
      {editingOrder && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50 backdrop-blur-sm">
          <div className="bg-white rounded-2xl w-full max-w-md shadow-xl overflow-hidden">
            <div className="p-4 border-b border-stone-100 flex justify-between items-center bg-stone-50">
              <h3 className="font-bold text-lg">
                تعديل الطلب #{editingOrder.scan_id?.substring(0, 6)}
              </h3>
              <button
                onClick={() => setEditingOrder(null)}
                className="text-stone-400 hover:text-stone-900 transition-colors"
              >
                <X size={20} />
              </button>
            </div>
            <div className="p-6 flex flex-col gap-4">
              <div>
                <label className="block text-sm font-medium text-stone-700 mb-1">اسم العميل</label>
                <input
                  type="text"
                  className="w-full p-2.5 border border-stone-200 rounded-lg outline-none focus:border-stone-900"
                  value={editForm.customer_name || ""}
                  onChange={(e) => setEditForm({ ...editForm, customer_name: e.target.value })}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-stone-700 mb-1">رقم الهاتف</label>
                <input
                  type="text"
                  className="w-full p-2.5 border border-stone-200 rounded-lg outline-none focus:border-stone-900"
                  dir="ltr"
                  value={editForm.customer_phone || ""}
                  onChange={(e) => setEditForm({ ...editForm, customer_phone: e.target.value })}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-stone-700 mb-1">الولاية</label>
                <input
                  type="text"
                  className="w-full p-2.5 border border-stone-200 rounded-lg outline-none focus:border-stone-900"
                  value={editForm.wilaya || ""}
                  onChange={(e) => setEditForm({ ...editForm, wilaya: e.target.value })}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-stone-700 mb-1">العنوان</label>
                <textarea
                  className="w-full p-2.5 border border-stone-200 rounded-lg outline-none focus:border-stone-900"
                  rows={3}
                  value={editForm.delivery_address || ""}
                  onChange={(e) => setEditForm({ ...editForm, delivery_address: e.target.value })}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-stone-700 mb-1">السعر</label>
                <input
                  type="number"
                  className="w-full p-2.5 border border-stone-200 rounded-lg outline-none focus:border-stone-900"
                  value={editForm.total_amount || 0}
                  onChange={(e) => setEditForm({ ...editForm, total_amount: Number(e.target.value) })}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-stone-700 mb-1">ملاحظات</label>
                <textarea
                  className="w-full p-2.5 border border-stone-200 rounded-lg outline-none focus:border-stone-900"
                  rows={2}
                  value={editForm.notes || ""}
                  onChange={(e) => setEditForm({ ...editForm, notes: e.target.value })}
                />
              </div>
            </div>
            <div className="p-4 border-t border-stone-100 flex justify-end gap-2 bg-stone-50">
              <button
                onClick={() => setEditingOrder(null)}
                className="px-4 py-2 rounded-lg text-stone-600 hover:bg-stone-200 transition-colors"
              >
                إلغاء
              </button>
              <button
                onClick={handleSaveEdit}
                className="px-4 py-2 rounded-lg bg-stone-900 text-white hover:bg-black transition-colors flex items-center gap-2"
              >
                <Save size={18} /> حفظ التغييرات
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Image Modal */}
      {viewingImage && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center p-4 z-50 backdrop-blur-sm" onClick={() => setViewingImage(null)}>
          <div className="relative max-w-4xl w-full max-h-[90vh] flex flex-col items-center">
            <button
              onClick={() => setViewingImage(null)}
              className="absolute -top-12 right-0 text-white/70 hover:text-white transition-colors"
            >
              <X size={32} />
            </button>
            <img
              src={viewingImage}
              alt="Waveform"
              className="rounded-lg shadow-2xl max-w-full max-h-[85vh] object-contain bg-white"
              onClick={(e) => e.stopPropagation()}
            />
            <a
              href={viewingImage}
              download
              className="mt-4 bg-white text-stone-900 px-6 py-2 rounded-full font-bold hover:bg-stone-200 transition-colors flex items-center gap-2"
              onClick={(e) => e.stopPropagation()}
            >
              <Download size={18} /> تحميل الصورة
            </a>
          </div>
        </div>
      )}

      {/* Hidden Global Audio Player */}
      <audio id="audio-player" onEnded={() => setPlayingAudio(null)} className="hidden" />
    </div>
  );
}
