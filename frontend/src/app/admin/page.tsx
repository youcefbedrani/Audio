"use client";

import { useState, useEffect } from "react";
import { 
  Search, Download, Play, Pause, ExternalLink, Plus, UserPlus, Trash2, 
  Edit, ChevronLeft, ChevronRight, X, Save, Users, Copy, 
  Settings as SettingsIcon, Music, Loader2, Calendar, Phone, MapPin, User, FileText
} from "lucide-react";
import AdminStats from "@/components/AdminStats";
import { 
  getOrders, updateOrderStatus, getConfirmationAgents, addConfirmationAgent, 
  deleteConfirmationAgent, deleteOrder, updateOrderDetails, getSettings, 
  updateSettings, getAdminStats, Settings, getAdminUsers, addAdminUser, 
  deleteAdminUser, createOrder 
} from "@/lib/api";
import { Order, AdminStatsData } from "@/lib/types";
import Login from "@/components/Login";

const ALGERIAN_WILAYAS = [
  "الجزائر", "البليدة", "وهران", "قسنطينة", "سطيف", "عنابة", "تيزي وزو", "بجاية", "باتنة", "بشار",
  "تبسة", "تلمسان", "الجلفة", "جيجل", "سعيدة", "سكيكدة", "سيدي بلعباس", "قالمة", "المدية", "مستغانم",
  "المسيلة", "معسكر", "ورقلة", "البيض", "إليزي", "برج بوعريريج", "بومرداس", "الطارف", "تندوف", "تيسمسيلت",
  "الوادي", "خنشلة", "سوق أهراس", "تيبازة", "ميلة", "عين الدفلى", "النعامة", "عين تيموشنت", "غرداية", "غليزان",
  "أدرار", "الشلف", "الأغواط", "أم البواقي", "تمنراست", "تيارت", "تيميمون", "برج باجي مختار", "أولاد جلال", 
  "بني عباس", "عين صالح", "عين قزام", "تقرت", "جانت", "المغير", "المنيعة"
];

const FRAME_TYPES = [
  { id: 1, title: "Simple Order (إطار خشبي بسيط)", price: 5500 },
  { id: 2, title: "VIP Order (إطار معدني راقي)", price: 6500 },
  { id: 3, title: "Handmade Order (إطار يدوي فاخر)", price: 7500 },
];

export default function AdminPage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [orders, setOrders] = useState<Order[]>([]);
  const [visibleOrders, setVisibleOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [playingAudio, setPlayingAudio] = useState<string | null>(null);
  const [viewingImage, setViewingImage] = useState<string | null>(null);

  // Pagination
  const [page, setPage] = useState(1);
  const [limit] = useState(30);
  const [totalPages, setTotalPages] = useState(1);
  const [totalOrders, setTotalOrders] = useState(0);

  // Edit Modal
  const [editingOrder, setEditingOrder] = useState<Order | null>(null);
  const [editForm, setEditForm] = useState<Partial<Order>>({});

  // Add Manual Order Modal & Form
  const [showAddOrderModal, setShowAddOrderModal] = useState(false);
  const [newOrderForm, setNewOrderForm] = useState({
    customer_name: "",
    customer_phone: "",
    wilaya: "",
    baladya: "",
    delivery_address: "",
    frame_id: 1,
    total_amount: 5500,
    confirmation_agent: "",
    notes: "",
  });
  const [newOrderAudio, setNewOrderAudio] = useState<File | null>(null);
  const [isCreatingOrder, setIsCreatingOrder] = useState(false);

  // Statistics
  const [adminStats, setAdminStats] = useState<AdminStatsData | null>(null);

  // Confirmation Agents
  const [agents, setAgents] = useState<string[]>([]);
  const [newAgentName, setNewAgentName] = useState("");

  // Pixel Settings
  const [pixelSettings, setPixelSettings] = useState<Settings>({ fb_pixel_id: "", tiktok_pixel_id: "" });
  const [isSavingSettings, setIsSavingSettings] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

  // Role and Agent State
  const [role, setRole] = useState("admin");
  const [agentName, setAgentName] = useState("");
  const [statusFilter, setStatusFilter] = useState("");

  // User credentials state
  const [adminUsers, setAdminUsers] = useState<any[]>([]);
  const [showUsersTab, setShowUsersTab] = useState(false);
  const [newEmail, setNewEmail] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [newRole, setNewRole] = useState("agent");
  const [newUserAgent, setNewUserAgent] = useState("");

  useEffect(() => {
    const savedAuth = localStorage.getItem("admin_authenticated");
    if (savedAuth === "true") {
      setIsAuthenticated(true);
      setRole(localStorage.getItem("admin_role") || "admin");
      setAgentName(localStorage.getItem("admin_agent_name") || "");
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

  const loadStats = async () => {
    try {
      const userRole = localStorage.getItem("admin_role") || "admin";
      const userAgentName = localStorage.getItem("admin_agent_name") || "";
      const stats = await getAdminStats(userRole === "agent" ? userAgentName : undefined);
      setAdminStats(stats);
    } catch (error) {
      console.error("Failed to load stats", error);
    }
  };

  // Initial load
  useEffect(() => {
    if (isAuthenticated) {
      const savedRole = localStorage.getItem("admin_role") || "admin";
      const savedAgentName = localStorage.getItem("admin_agent_name") || "";
      setRole(savedRole);
      setAgentName(savedAgentName);
      fetchOrders();
      getConfirmationAgents().then(setAgents);
      loadSettings();
      loadStats();
    }
  }, [isAuthenticated]);

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

  const fetchOrders = async (silent = false) => {
    if (!silent) setLoading(true);
    try {
      const userRole = localStorage.getItem("admin_role") || "admin";
      const userAgentName = localStorage.getItem("admin_agent_name") || "";
      const activeAgent = userRole === "agent" ? userAgentName : undefined;
      
      const data: any = await getOrders(page, limit, searchTerm, statusFilter, activeAgent);

      if (data && data.orders) {
        setOrders(data.orders);
        setVisibleOrders(data.orders);
        setTotalPages(data.total_pages);
        setTotalOrders(data.total);
      } else {
        const ordersArr = Array.isArray(data) ? data : (data.results || []);
        if (JSON.stringify(ordersArr) !== JSON.stringify(orders)) {
          setOrders(ordersArr);
          setVisibleOrders(ordersArr);
        }
      }
    } catch (error: any) {
      console.error("[Admin] Failed to load orders:", error);
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

  const fetchAdminUsers = async () => {
    try {
      const data = await getAdminUsers();
      setAdminUsers(data || []);
    } catch (error) {
      console.error("Failed to load admin credentials", error);
    }
  };

  const handleAddAdminUser = async () => {
    if (!newEmail || !newPassword) return;
    try {
      await addAdminUser({
        email: newEmail,
        password: newPassword,
        role: newRole,
        agent_name: newRole === "agent" ? newUserAgent : ""
      });
      alert("تمت إضافة حساب بنجاح");
      setNewEmail("");
      setNewPassword("");
      setNewRole("agent");
      setNewUserAgent("");
      fetchAdminUsers();
    } catch (error: any) {
      alert(error.response?.data?.error || "فشل إضافة حساب");
    }
  };

  const handleDeleteAdminUser = async (email: string) => {
    if (!confirm(`هل أنت متأكد من حذف الحساب "${email}"؟`)) return;
    try {
      await deleteAdminUser(email);
      fetchAdminUsers();
    } catch (error: any) {
      alert(error.response?.data?.error || "فشل حذف الحساب");
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      loadAgents();
      loadSettings();
      loadStats();
      const currentRole = localStorage.getItem("admin_role") || "admin";
      if (currentRole === "admin") {
        fetchAdminUsers();
      }

      const debounceTimer = setTimeout(() => {
        fetchOrders(false);
      }, 500);

      const interval = setInterval(() => {
        if (!document.hidden) {
          fetchOrders(true);
          loadStats();
        }
      }, 30000);

      return () => {
        clearTimeout(debounceTimer);
        clearInterval(interval);
      };
    }
  }, [isAuthenticated, page, searchTerm, statusFilter, role]);

  const handleAddAgent = async () => {
    const trimmedName = newAgentName.trim();
    if (!trimmedName) return;

    const prevAgents = [...agents];
    setAgents([...agents, trimmedName]);
    setNewAgentName("");

    try {
      await addConfirmationAgent(trimmedName);
    } catch (error) {
      alert("فشل إضافة الاسم");
      setAgents(prevAgents);
    }
  };

  const handleDeleteAgent = async (name: string) => {
    if (!confirm(`هل أنت متأكد من حذف المكلف "${name}"؟`)) return;

    const prevAgents = [...agents];
    setAgents(agents.filter(a => a !== name));

    try {
      await deleteConfirmationAgent(name);
    } catch (error) {
      alert("فشل حذف المكلف");
      setAgents(prevAgents);
    }
  };

  const handleDeleteOrder = async (orderId: string | number) => {
    if (!confirm("هل أنت متأكد من حذف هذا الطلب؟")) return;
    try {
      await deleteOrder(orderId);
      const filterList = (list: Order[]) => list.filter((o) => o.id !== orderId);
      setOrders((prev) => filterList(prev));
      setVisibleOrders((prev) => filterList(prev));
      setTotalOrders((prev) => prev - 1);
      loadStats();
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
      const updateList = (list: Order[]) =>
        list.map((o) =>
          o.id === editingOrder.id ? { ...o, ...editForm } : o
        );

      setOrders((prev) => updateList(prev));
      setVisibleOrders((prev) => updateList(prev));
      setEditingOrder(null);
      loadStats();
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
      const updatedOrder = { ...currentOrder, status: newStatus as Order['status'], confirmation_agent: newAgent };
      const updateList = (list: Order[]) =>
        list.map((o) => (o.id === orderId ? updatedOrder : o));

      setOrders((prev) => updateList(prev));
      setVisibleOrders((prev) => updateList(prev));

      await updateOrderStatus(orderId, newStatus as string, newAgent);
      loadStats();
    } catch (error) {
      console.error("Failed to update order", error);
      fetchOrders();
      alert("حدث خطأ أثناء التحديث");
    }
  };

  const handleCreateOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newOrderForm.customer_name || !newOrderForm.customer_phone || !newOrderForm.wilaya || !newOrderForm.delivery_address) {
      alert("يرجى تعبئة الحقول الإلزامية المطلوبة (*) أولاً");
      return;
    }

    setIsCreatingOrder(true);
    try {
      const selectedFrame = FRAME_TYPES.find(f => f.id === Number(newOrderForm.frame_id));
      const payload: any = {
        customer_name: newOrderForm.customer_name.trim(),
        customer_phone: newOrderForm.customer_phone.trim(),
        wilaya: newOrderForm.wilaya,
        baladya: newOrderForm.baladya.trim() || newOrderForm.wilaya,
        delivery_address: newOrderForm.delivery_address.trim(),
        frame_id: Number(newOrderForm.frame_id),
        frame_title: selectedFrame?.title?.split(" (")[0] || "Simple Order",
        frame_type: newOrderForm.frame_id === 1 ? "simple" : newOrderForm.frame_id === 2 ? "vip" : "handmade",
        total_amount: Number(newOrderForm.total_amount),
        notes: newOrderForm.notes.trim(),
        status: "pending",
        confirmation_agent: newOrderForm.confirmation_agent || undefined
      };

      await createOrder(payload, newOrderAudio || undefined);
      
      alert("تم تسجيل الطلب اليدوي بنجاح!");
      
      // Reset form
      setNewOrderForm({
        customer_name: "",
        customer_phone: "",
        wilaya: "",
        baladya: "",
        delivery_address: "",
        frame_id: 1,
        total_amount: 5500,
        confirmation_agent: "",
        notes: "",
      });
      setNewOrderAudio(null);
      setShowAddOrderModal(false);
      
      // Refresh page
      fetchOrders();
      loadStats();
    } catch (err: any) {
      console.error("Error creating manual order:", err);
      alert(err.response?.data?.error || "فشل تسجيل الطلب الجديد. يرجى المحاولة لاحقاً.");
    } finally {
      setIsCreatingOrder(false);
    }
  };

  const handleFrameChange = (frameId: number) => {
    const selected = FRAME_TYPES.find(f => f.id === frameId);
    setNewOrderForm({
      ...newOrderForm,
      frame_id: frameId,
      total_amount: selected ? selected.price : 5500
    });
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
    localStorage.removeItem("admin_role");
    localStorage.removeItem("admin_agent_name");
    setIsAuthenticated(false);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  if (!isAuthenticated) {
    return <Login onLogin={() => setIsAuthenticated(true)} />;
  }

  return (
    <div className="min-h-screen bg-[#0B0F17] text-white p-4 sm:p-8 md:p-12 font-cairo relative overflow-hidden" dir="rtl">
      {/* Background radial glow */}
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-[#D4AF37]/5 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-blue-500/5 rounded-full blur-3xl pointer-events-none" />

      <div className="max-w-7xl mx-auto relative z-10">
        {/* Header */}
        <header className="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-8 gap-6 bg-[#121926]/90 border border-[#D4AF37]/10 p-6 rounded-3xl backdrop-blur-md shadow-xl">
          <div className="flex flex-col gap-1">
            <h1 className="text-2xl font-bold tracking-wide font-amiri flex items-center gap-3">
              <span className="gold-text">رويسية فويس</span>
              <span className="text-xs font-normal text-stone-400 border border-stone-800 px-2 py-0.5 rounded-full">
                {role === "admin" ? "لوحة الإدارة الكاملة" : "فضاء الوكيل"}
              </span>
            </h1>
            <p className="text-xs text-stone-400">
              {role === "admin" 
                ? "إدارة طلبات إطارات الموجات الصوتية ومتابعة الأداء وإعدادات البيكسل" 
                : `أهلاً بك الموظف (${agentName}) - محطة تأكيد ومتابعة الطلبات المخصصة لك`}
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3 w-full lg:w-auto justify-end">
            {role === "admin" && (
              <button
                onClick={() => setShowAddOrderModal(true)}
                className="px-4 py-2.5 bg-gradient-to-r from-[#BF953F] to-[#AA771C] text-[#111] font-bold rounded-xl hover:brightness-110 active:scale-[0.98] transition-all flex items-center gap-2 shadow-lg shadow-amber-950/20 text-xs sm:text-sm"
              >
                <Plus size={16} />
                <span>إدخال طلب جديد</span>
              </button>
            )}

            {role === "admin" && (
              <button
                onClick={() => setShowUsersTab(!showUsersTab)}
                className={`p-2.5 bg-[#172030] border border-stone-800 rounded-xl hover:bg-[#1f2b40] transition-all shadow-sm ${showUsersTab ? 'text-[#D4AF37] border-[#D4AF37]/30' : 'text-stone-300'}`}
                title="إدارة الحسابات وصلاحيات الدخول"
              >
                <Users size={18} />
              </button>
            )}

            {role === "admin" && (
              <button
                onClick={() => setShowSettings(!showSettings)}
                className={`p-2.5 bg-[#172030] border border-stone-800 rounded-xl hover:bg-[#1f2b40] transition-all shadow-sm ${showSettings ? 'text-[#D4AF37] border-[#D4AF37]/30' : 'text-stone-300'}`}
                title="إعدادات البيكسل"
              >
                <SettingsIcon size={18} />
              </button>
            )}

            <button
              onClick={handleLogout}
              className="px-4 py-2.5 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/20 rounded-xl font-bold transition-all text-xs sm:text-sm"
            >
              تسجيل الخروج
            </button>
          </div>
        </header>

        {/* Pixel settings overlay */}
        {showSettings && role === "admin" && (
          <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-[#121926] border border-[#D4AF37]/20 p-6 rounded-3xl shadow-2xl w-full max-w-md animate-in fade-in zoom-in-95 duration-200">
              <div className="flex justify-between items-center mb-5 border-b border-stone-800 pb-3">
                <h3 className="font-bold text-white font-amiri text-lg flex items-center gap-2">
                  <SettingsIcon className="text-[#D4AF37] w-5 h-5" />
                  إعدادات بيكسل التتبع
                </h3>
                <button onClick={() => setShowSettings(false)} className="text-stone-400 hover:text-white transition-colors">
                  <X size={20} />
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-stone-300 mb-2">Facebook Pixel ID</label>
                  <input
                    type="text"
                    className="w-full px-4 py-2.5 bg-[#172030] text-white border border-stone-850 rounded-xl focus:ring-1 focus:ring-[#D4AF37] focus:border-[#D4AF37] outline-none text-sm"
                    placeholder="Enter Facebook Pixel ID..."
                    value={pixelSettings.fb_pixel_id}
                    onChange={(e) => setPixelSettings({ ...pixelSettings, fb_pixel_id: e.target.value })}
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-stone-300 mb-2">TikTok Pixel ID</label>
                  <input
                    type="text"
                    className="w-full px-4 py-2.5 bg-[#172030] text-white border border-stone-850 rounded-xl focus:ring-1 focus:ring-[#D4AF37] focus:border-[#D4AF37] outline-none text-sm"
                    placeholder="Enter TikTok Pixel ID..."
                    value={pixelSettings.tiktok_pixel_id}
                    onChange={(e) => setPixelSettings({ ...pixelSettings, tiktok_pixel_id: e.target.value })}
                  />
                </div>

                <div className="pt-2 flex gap-3">
                  <button
                    onClick={() => setShowSettings(false)}
                    className="flex-1 py-2.5 bg-[#172030] hover:bg-[#1f2b40] text-stone-300 rounded-xl font-bold transition-all text-xs"
                  >
                    إلغاء
                  </button>
                  <button
                    onClick={handleSaveSettings}
                    disabled={isSavingSettings}
                    className="flex-1 py-2.5 bg-gradient-to-r from-[#BF953F] to-[#AA771C] text-[#111] rounded-xl font-bold hover:brightness-110 transition-all text-xs disabled:opacity-50 flex items-center justify-center gap-2"
                  >
                    {isSavingSettings && <Loader2 className="animate-spin" size={14} />}
                    <span>حفظ التغييرات</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Credentials and roles overlay */}
        {showUsersTab && role === "admin" && (
          <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-[#121926] border border-[#D4AF37]/20 p-6 rounded-3xl shadow-2xl w-full max-w-lg animate-in fade-in zoom-in-95 duration-200 flex flex-col max-h-[85vh]">
              <div className="flex justify-between items-center mb-4 border-b border-stone-800 pb-3">
                <h3 className="font-bold text-white font-amiri text-lg flex items-center gap-2">
                  <Users className="text-[#D4AF37] w-5 h-5" />
                  إدارة حسابات الدخول والصلاحيات
                </h3>
                <button onClick={() => setShowUsersTab(false)} className="text-stone-400 hover:text-white transition-colors">
                  <X size={20} />
                </button>
              </div>

              {/* Users scroll container */}
              <div className="flex-1 overflow-y-auto mb-4 space-y-3 pr-1">
                {adminUsers.map((user: any) => (
                  <div key={user.email} className="flex justify-between items-center p-3 bg-[#172030] border border-stone-850 rounded-xl">
                    <div className="flex flex-col gap-0.5">
                      <span className="text-xs font-bold text-stone-200 font-sans">{user.email}</span>
                      <span className="text-[10px] text-stone-400">
                        {user.role === "admin" ? (
                          <span className="text-amber-400 font-bold">مدير كامل الصلاحيات (Admin)</span>
                        ) : (
                          <span>مكلف تأكيد (Agent): <strong className="text-blue-400">{user.agent_name || "غير محدد"}</strong></span>
                        )}
                      </span>
                    </div>
                    <button
                      onClick={() => handleDeleteAdminUser(user.email)}
                      className="text-rose-400 hover:bg-rose-500/10 p-2 rounded-lg transition-colors border border-rose-500/15"
                      title="حذف الحساب"
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                ))}
              </div>

              {/* Add User Form */}
              <div className="bg-[#172030] p-4 rounded-2xl border border-stone-850 space-y-4">
                <h4 className="text-xs font-bold text-[#D4AF37] border-r-2 border-[#D4AF37] pr-2">إضافة حساب جديد:</h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="block text-[10px] font-semibold text-stone-300 mb-1">البريد الإلكتروني</label>
                    <input
                      type="email"
                      className="w-full p-2 bg-[#121926] border border-stone-800 rounded-lg text-xs outline-none text-white focus:border-[#D4AF37]"
                      placeholder="user@example.com"
                      value={newEmail}
                      onChange={(e) => setNewEmail(e.target.value)}
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] font-semibold text-stone-300 mb-1">كلمة المرور</label>
                    <input
                      type="password"
                      className="w-full p-2 bg-[#121926] border border-stone-800 rounded-lg text-xs outline-none text-white focus:border-[#D4AF37]"
                      placeholder="••••••"
                      value={newPassword}
                      onChange={(e) => setNewPassword(e.target.value)}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="block text-[10px] font-semibold text-stone-300 mb-1">نوع الصلاحية</label>
                    <select
                      className="w-full p-2 bg-[#121926] border border-stone-800 rounded-lg text-xs outline-none text-white focus:border-[#D4AF37]"
                      value={newRole}
                      onChange={(e) => setNewRole(e.target.value)}
                    >
                      <option value="admin">مدير كامل (Admin)</option>
                      <option value="agent">مكلف تأكيد (Agent)</option>
                    </select>
                  </div>
                  
                  {newRole === "agent" && (
                    <div>
                      <label className="block text-[10px] font-semibold text-stone-300 mb-1">الربط بملف وكيل</label>
                      <select
                        className="w-full p-2 bg-[#121926] border border-stone-800 rounded-lg text-xs outline-none text-white focus:border-[#D4AF37]"
                        value={newUserAgent}
                        onChange={(e) => setNewUserAgent(e.target.value)}
                      >
                        <option value="">اختر من فريق العمل...</option>
                        {agents.map((agent) => (
                          <option key={agent} value={agent}>{agent}</option>
                        ))}
                      </select>
                    </div>
                  )}
                </div>

                <button
                  onClick={handleAddAdminUser}
                  className="w-full py-2 bg-gradient-to-r from-[#BF953F] to-[#AA771C] text-[#111] font-bold rounded-lg hover:brightness-110 transition-all text-xs"
                >
                  إنشاء حساب دخول جديد
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Statistics Cards */}
        <AdminStats stats={adminStats} role={role} />

        {/* Filters and Management */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-8">
          {/* Work Team Management - Only Visible to Admin */}
          {role === "admin" && (
            <div className="lg:col-span-4 bg-[#121926]/90 border border-[#D4AF37]/10 p-5 rounded-3xl backdrop-blur-md shadow-xl flex flex-col">
              <h3 className="text-sm font-bold text-white mb-3 flex items-center gap-2 border-r-4 border-[#D4AF37] pr-2">
                <Users size={16} className="text-[#D4AF37]" />
                فريق عمل التأكيد
              </h3>

              {/* Team Members Tag Clouds */}
              <div className="flex flex-wrap gap-2 mb-4 overflow-y-auto max-h-36 pr-1 flex-1">
                {agents.map(agent => (
                  <div 
                    key={agent} 
                    className="flex items-center gap-1.5 px-3 py-1 bg-[#172030] border border-stone-800 text-stone-300 rounded-full text-xs font-medium hover:border-[#D4AF37]/30 transition-all group"
                  >
                    <span>{agent}</span>
                    <button
                      onClick={() => handleDeleteAgent(agent)}
                      className="text-stone-500 hover:text-rose-400 transition-colors"
                      title="حذف المكلف"
                    >
                      <X size={12} />
                    </button>
                  </div>
                ))}
                {agents.length === 0 && (
                  <span className="text-xs text-stone-500 italic py-4">لم يتم تعيين أي وكيل تأكيد بعد.</span>
                )}
              </div>

              {/* Add Team Member Input */}
              <div className="flex gap-2 pt-2 border-t border-stone-850">
                <div className="relative flex-1">
                  <UserPlus className="absolute right-3 top-2.5 text-stone-500" size={14} />
                  <input
                    type="text"
                    placeholder="إضافة اسم وكيل جديد..."
                    className="w-full py-2 pr-9 pl-3 rounded-xl bg-[#172030] border border-stone-800 text-xs text-white outline-none focus:border-[#D4AF37] placeholder:text-stone-500"
                    value={newAgentName}
                    onChange={(e) => setNewAgentName(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleAddAgent()}
                  />
                </div>
                <button
                  onClick={handleAddAgent}
                  className="bg-gradient-to-r from-[#BF953F] to-[#AA771C] text-[#111] px-3.5 rounded-xl hover:brightness-110 active:scale-[0.97] transition-all"
                >
                  <Plus size={16} />
                </button>
              </div>
            </div>
          )}

          {/* Orders Filter Controls & Search */}
          <div className={`${role === "admin" ? "lg:col-span-8" : "lg:col-span-12"} bg-[#121926]/90 border border-[#D4AF37]/10 p-5 rounded-3xl backdrop-blur-md shadow-xl flex flex-col justify-center`}>
            <h3 className="text-sm font-bold text-white mb-4 flex items-center gap-2 border-r-4 border-[#D4AF37] pr-2">
              <Search size={16} className="text-[#D4AF37]" />
              البحث والتصفية
            </h3>

            <div className="flex flex-col sm:flex-row gap-3">
              <div className="relative flex-1">
                <Search className="absolute right-3.5 top-3 text-stone-500" size={16} />
                <input
                  type="text"
                  placeholder="بحث باسم العميل، رقم الهاتف، أو كود الممسوح..."
                  className="w-full py-2.5 pr-10 pl-4 rounded-xl bg-[#172030] border border-stone-800 text-xs text-white outline-none focus:border-[#D4AF37] placeholder:text-stone-500"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>

              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="bg-[#172030] border border-stone-800 rounded-xl px-4 py-2.5 text-xs font-semibold text-stone-300 outline-none focus:border-[#D4AF37] cursor-pointer"
              >
                <option value="">جميع حالات الطلبات</option>
                <option value="pending">قيد الانتظار</option>
                <option value="confirmed">تم التأكيد</option>
                <option value="cancelled">ملغى</option>
                <option value="no_response">لا يوجد رد</option>
                <option value="shipped">تم الشحن</option>
                <option value="delivered">تم التوصيل</option>
              </select>

              <button
                onClick={exportToCSV}
                className="bg-[#172030] hover:bg-[#1f2b40] border border-stone-800 text-stone-200 px-4 py-2.5 rounded-xl transition-all flex items-center justify-center gap-2 font-bold text-xs"
              >
                <Download size={16} className="text-emerald-400" />
                <span>تحميل CSV</span>
              </button>
            </div>
          </div>
        </div>

        {/* Orders Table Container */}
        {loading ? (
          <div className="flex flex-col items-center justify-center py-24 bg-[#121926]/50 border border-[#D4AF37]/10 rounded-3xl shadow-xl">
            <Loader2 className="animate-spin text-[#D4AF37] mb-3" size={32} />
            <div className="text-stone-400 text-sm">جاري تحميل بيانات الطلبات والربط بالخادم...</div>
          </div>
        ) : (
          <div className="bg-[#121926]/90 border border-[#D4AF37]/10 rounded-3xl shadow-xl overflow-hidden backdrop-blur-md">
            <div className="overflow-x-auto">
              <table className="w-full text-right text-sm">
                <thead className="bg-[#172030] text-stone-400 font-semibold border-b border-stone-800">
                  <tr>
                    <th className="p-4 rounded-tr-3xl">معلومات الطلب</th>
                    <th className="p-4">العميل</th>
                    <th className="p-4">العنوان والولاية</th>
                    <th className="p-4">نوع الإطار والسعر</th>
                    {role === "admin" && <th className="p-4">المكلف بالتأكيد</th>}
                    <th className="p-4">حالة الطلب</th>
                    <th className="p-4 rounded-tl-3xl">إجراءات</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-stone-800/40">
                  {visibleOrders.map((order) => (
                    <tr key={order.id} className="hover:bg-[#172030]/30 transition-colors">
                      {/* ID / Code / Audio */}
                      <td className="p-4 align-top">
                        <div className="flex flex-col gap-2">
                          <div className="flex items-center gap-2">
                            <span className="font-mono font-bold text-xs bg-[#1a2536] border border-stone-850 px-2.5 py-1 rounded-lg text-[#D4AF37] tracking-wider flex items-center gap-2">
                              <span>#{order.scan_id || '---'}</span>
                              {order.scan_id && (
                                <button 
                                  onClick={() => copyToClipboard(order.scan_id!)} 
                                  className="text-stone-500 hover:text-white transition-colors" 
                                  title="نسخ معرف المسح"
                                >
                                  <Copy size={11} />
                                </button>
                              )}
                            </span>
                            <span className="text-[10px] text-stone-500 font-sans">ID: {order.id}</span>
                          </div>
                          
                          <div className="text-[10px] text-stone-400 font-sans flex items-center gap-1">
                            <Calendar size={11} className="text-stone-500" />
                            <span>{order.created_at ? new Date(order.created_at).toLocaleDateString("ar-DZ") : "N/A"}</span>
                          </div>

                          <div className="flex items-center gap-2 mt-1">
                            {order.audio_file_url ? (
                              <button
                                onClick={() => toggleAudio(order.audio_file_url!)}
                                className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[10px] font-bold border transition-all ${
                                  playingAudio === order.audio_file_url
                                    ? "bg-[#D4AF37] text-[#111] border-[#D4AF37]"
                                    : "bg-[#172030] hover:bg-[#1f2b40] text-stone-300 border-stone-800"
                                }`}
                              >
                                {playingAudio === order.audio_file_url ? <Pause size={11} /> : <Play size={11} />}
                                <span>{playingAudio === order.audio_file_url ? "توقف" : "استماع"}</span>
                              </button>
                            ) : (
                              <span className="text-[10px] text-stone-500 italic">لا يوجد تسجيل</span>
                            )}

                            {order.qr_code_url && (
                              <button
                                onClick={() => setViewingImage(order.qr_code_url!)}
                                className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20 hover:bg-blue-500/20 text-[10px] font-bold transition-all"
                                title="معاينة كود الموجة"
                              >
                                <ExternalLink size={11} />
                                <span>كود الموجة</span>
                              </button>
                            )}
                          </div>
                        </div>
                      </td>

                      {/* Customer Info */}
                      <td className="p-4 align-top">
                        <div className="font-bold text-white text-xs sm:text-sm">{order.customer_name}</div>
                        <div className="text-stone-400 font-sans text-xs mt-1 flex items-center gap-1.5" dir="ltr">
                          <Phone size={11} className="text-stone-500" />
                          <span>{order.customer_phone}</span>
                        </div>
                        {order.customer_email && (
                          <div className="text-[10px] text-stone-500 font-sans truncate max-w-[140px] mt-0.5">
                            {order.customer_email}
                          </div>
                        )}
                      </td>

                      {/* Location Details */}
                      <td className="p-4 align-top">
                        <div className="text-stone-200 text-xs font-semibold flex items-center gap-1">
                          <MapPin size={12} className="text-[#D4AF37]" />
                          <span>{order.wilaya}</span>
                          {order.baladya && order.baladya !== order.wilaya && (
                            <span className="text-stone-400 text-[10px]"> - {order.baladya}</span>
                          )}
                        </div>
                        <div className="text-stone-400 text-[11px] mt-1.5 max-w-[180px] leading-relaxed line-clamp-2" title={order.delivery_address}>
                          {order.delivery_address}
                        </div>
                        {order.notes && (
                          <div className="text-[10px] bg-amber-500/5 border border-amber-500/15 text-[#D4AF37]/90 px-2 py-1 rounded-lg mt-2 max-w-[180px] break-words">
                            <strong>ملاحظة:</strong> {order.notes}
                          </div>
                        )}
                      </td>

                      {/* Frame type and pricing */}
                      <td className="p-4 align-top">
                        <div className="font-bold text-[#D4AF37] text-xs sm:text-sm font-sans">{order.total_amount?.toLocaleString()} د.ج</div>
                        <div className="text-[10px] text-stone-400 mt-1.5 flex items-center gap-1">
                          <FileText size={10} className="text-stone-500" />
                          <span>
                            {order.frame_id === 1 ? "Simple Frame" :
                             order.frame_id === 2 ? "VIP Frame" :
                             order.frame_id === 3 ? "Handmade Frame" :
                             order.frame_title || "Unknown"}
                          </span>
                        </div>
                      </td>

                      {/* Confirmation Agent - Only editable by Admin */}
                      {role === "admin" && (
                        <td className="p-4 align-top">
                          <select
                            value={order.confirmation_agent || ""}
                            onChange={(e) =>
                              handleUpdateStatus(order.id, { confirmation_agent: e.target.value })
                            }
                            className="bg-[#172030] border border-stone-800 text-stone-300 rounded-lg px-2 py-1 text-xs w-28 cursor-pointer outline-none focus:border-[#D4AF37]"
                          >
                            <option value="">تعيين وكيل...</option>
                            {agents.map((agent) => (
                              <option key={agent} value={agent}>{agent}</option>
                            ))}
                          </select>
                        </td>
                      )}

                      {/* Status select - Editable by both but differently styled */}
                      <td className="p-4 align-top">
                        <select
                          value={order.status}
                          onChange={(e) => handleUpdateStatus(order.id, { status: e.target.value })}
                          className={`
                            px-2 py-1.5 rounded-lg text-[10px] font-bold border outline-none cursor-pointer w-28 text-center transition-all
                            ${order.status === "pending"
                              ? "bg-yellow-500/10 text-yellow-400 border-yellow-500/20"
                              : order.status === "confirmed"
                                ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                                : order.status === "cancelled"
                                  ? "bg-rose-500/10 text-rose-400 border-rose-500/20"
                                  : order.status === "no_response"
                                    ? "bg-amber-500/10 text-amber-400 border-amber-500/20"
                                    : order.status === "shipped"
                                      ? "bg-indigo-500/10 text-indigo-400 border-indigo-500/20"
                                      : "bg-cyan-500/10 text-cyan-400 border-cyan-500/20"
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

                      {/* Actions */}
                      <td className="p-4 align-top">
                        <div className="flex gap-2">
                          <button
                            onClick={() => openEditModal(order)}
                            className="text-blue-400 hover:bg-blue-500/10 p-1.5 rounded-lg border border-blue-500/10 transition-colors"
                            title="تعديل تفاصيل الطلب"
                          >
                            <Edit size={14} />
                          </button>
                          
                          {role === "admin" && (
                            <button
                              onClick={() => handleDeleteOrder(order.id)}
                              className="text-rose-400 hover:bg-rose-500/10 p-1.5 rounded-lg border border-rose-500/10 transition-colors"
                              title="حذف الطلب نهائياً"
                            >
                              <Trash2 size={14} />
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {visibleOrders.length === 0 && (
                <div className="text-center py-20 text-stone-500 italic">لا توجد أي طلبات مطابقة للبحث أو معينة حالياً.</div>
              )}

              {/* Pagination Controls */}
              <div className="p-5 border-t border-stone-850 flex justify-between items-center bg-[#172030]/50">
                <button
                  disabled={page <= 1}
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-[#172030] border border-stone-850 text-xs font-semibold text-stone-300 disabled:opacity-40 hover:bg-[#1f2b40] transition-colors"
                >
                  <ChevronRight size={14} /> السابق
                </button>

                <span className="text-xs font-bold text-stone-400 font-sans">
                  صفحة {page} من {totalPages} (إجمالي الطلبات: {totalOrders})
                </span>

                <button
                  disabled={page >= totalPages}
                  onClick={() => setPage((p) => p + 1)}
                  className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-[#172030] border border-stone-850 text-xs font-semibold text-stone-300 disabled:opacity-40 hover:bg-[#1f2b40] transition-colors"
                >
                  التالي <ChevronLeft size={14} />
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Admin Manual Order Creation Modal */}
      {showAddOrderModal && role === "admin" && (
        <div className="fixed inset-0 bg-black/75 flex items-center justify-center p-4 z-50 backdrop-blur-sm">
          <div className="bg-[#121926] border border-[#D4AF37]/20 rounded-3xl w-full max-w-2xl shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
            <div className="p-5 border-b border-stone-800 flex justify-between items-center bg-[#172030]/50">
              <h3 className="font-bold text-lg font-amiri text-white flex items-center gap-2">
                <Plus size={20} className="text-[#D4AF37]" />
                إدخال طلب جديد يدوياً للمستودع
              </h3>
              <button
                onClick={() => setShowAddOrderModal(false)}
                className="text-stone-400 hover:text-white transition-colors"
              >
                <X size={20} />
              </button>
            </div>
            
            <form onSubmit={handleCreateOrder}>
              <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-4 max-h-[70vh] overflow-y-auto pr-2">
                {/* Customer Name */}
                <div>
                  <label className="block text-xs font-semibold text-stone-300 mb-1.5">اسم العميل بالكامل *</label>
                  <input
                    type="text"
                    required
                    className="w-full px-3 py-2 bg-[#172030] text-white border border-stone-800 rounded-xl focus:ring-1 focus:ring-[#D4AF37] focus:border-[#D4AF37] outline-none text-xs"
                    placeholder="مثال: يوسف بدراني"
                    value={newOrderForm.customer_name}
                    onChange={(e) => setNewOrderForm({ ...newOrderForm, customer_name: e.target.value })}
                  />
                </div>

                {/* Customer Phone */}
                <div>
                  <label className="block text-xs font-semibold text-stone-300 mb-1.5">رقم الهاتف للاتصال والتوصيل *</label>
                  <input
                    type="text"
                    required
                    className="w-full px-3 py-2 bg-[#172030] text-white border border-stone-800 rounded-xl focus:ring-1 focus:ring-[#D4AF37] focus:border-[#D4AF37] outline-none text-xs text-left"
                    dir="ltr"
                    placeholder="0661234567"
                    value={newOrderForm.customer_phone}
                    onChange={(e) => setNewOrderForm({ ...newOrderForm, customer_phone: e.target.value })}
                  />
                </div>

                {/* Wilaya select dropdown */}
                <div>
                  <label className="block text-xs font-semibold text-stone-300 mb-1.5">الولاية *</label>
                  <select
                    required
                    className="w-full px-3 py-2 bg-[#172030] text-white border border-stone-800 rounded-xl focus:ring-1 focus:ring-[#D4AF37] focus:border-[#D4AF37] outline-none text-xs cursor-pointer"
                    value={newOrderForm.wilaya}
                    onChange={(e) => setNewOrderForm({ ...newOrderForm, wilaya: e.target.value })}
                  >
                    <option value="">اختر الولاية...</option>
                    {ALGERIAN_WILAYAS.map(w => (
                      <option key={w} value={w}>{w}</option>
                    ))}
                  </select>
                </div>

                {/* Baladya input */}
                <div>
                  <label className="block text-xs font-semibold text-stone-300 mb-1.5">البلدية</label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 bg-[#172030] text-white border border-stone-800 rounded-xl focus:ring-1 focus:ring-[#D4AF37] focus:border-[#D4AF37] outline-none text-xs"
                    placeholder="مثال: حسين داي"
                    value={newOrderForm.baladya}
                    onChange={(e) => setNewOrderForm({ ...newOrderForm, baladya: e.target.value })}
                  />
                </div>

                {/* Full Delivery Address */}
                <div className="md:col-span-2">
                  <label className="block text-xs font-semibold text-stone-300 mb-1.5">عنوان التوصيل التفصيلي *</label>
                  <textarea
                    required
                    rows={2}
                    className="w-full px-3 py-2 bg-[#172030] text-white border border-stone-800 rounded-xl focus:ring-1 focus:ring-[#D4AF37] focus:border-[#D4AF37] outline-none text-xs resize-none"
                    placeholder="اكتب الشارع، رقم المنزل أو أي معالم واضحة تساعد عامل التوصيل..."
                    value={newOrderForm.delivery_address}
                    onChange={(e) => setNewOrderForm({ ...newOrderForm, delivery_address: e.target.value })}
                  />
                </div>

                {/* Frame Type selector */}
                <div>
                  <label className="block text-xs font-semibold text-stone-300 mb-1.5">نوع الإطار الفني *</label>
                  <select
                    className="w-full px-3 py-2 bg-[#172030] text-white border border-stone-800 rounded-xl focus:ring-1 focus:ring-[#D4AF37] focus:border-[#D4AF37] outline-none text-xs cursor-pointer"
                    value={newOrderForm.frame_id}
                    onChange={(e) => handleFrameChange(Number(e.target.value))}
                  >
                    {FRAME_TYPES.map(f => (
                      <option key={f.id} value={f.id}>{f.title} ({f.price} د.ج)</option>
                    ))}
                  </select>
                </div>

                {/* Editable Total Price */}
                <div>
                  <label className="block text-xs font-semibold text-stone-300 mb-1.5">سعر الطلب الإجمالي (د.ج)</label>
                  <input
                    type="number"
                    className="w-full px-3 py-2 bg-[#172030] text-white border border-stone-800 rounded-xl focus:ring-1 focus:ring-[#D4AF37] focus:border-[#D4AF37] outline-none text-xs font-sans"
                    value={newOrderForm.total_amount}
                    onChange={(e) => setNewOrderForm({ ...newOrderForm, total_amount: Number(e.target.value) })}
                  />
                </div>

                {/* Pre-assign Agent */}
                <div>
                  <label className="block text-xs font-semibold text-stone-300 mb-1.5">تعيين الموظف المكلف</label>
                  <select
                    className="w-full px-3 py-2 bg-[#172030] text-white border border-stone-800 rounded-xl focus:ring-1 focus:ring-[#D4AF37] focus:border-[#D4AF37] outline-none text-xs cursor-pointer"
                    value={newOrderForm.confirmation_agent}
                    onChange={(e) => setNewOrderForm({ ...newOrderForm, confirmation_agent: e.target.value })}
                  >
                    <option value="">اختر الموظف...</option>
                    {agents.map(a => (
                      <option key={a} value={a}>{a}</option>
                    ))}
                  </select>
                </div>

                {/* Optional Audio upload */}
                <div>
                  <label className="block text-xs font-semibold text-stone-300 mb-1.5 flex items-center gap-1.5">
                    <Music size={12} className="text-[#D4AF37]" />
                    ملف الصوت المرفق (اختياري)
                  </label>
                  <input
                    type="file"
                    accept="audio/*"
                    className="w-full text-xs text-stone-400 file:ml-4 file:py-2 file:px-3 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-[#1a2536] file:text-[#D4AF37] hover:file:bg-[#25354e] file:cursor-pointer"
                    onChange={(e) => {
                      if (e.target.files && e.target.files.length > 0) {
                        setNewOrderAudio(e.target.files[0]);
                      } else {
                        setNewOrderAudio(null);
                      }
                    }}
                  />
                </div>

                {/* Notes */}
                <div className="md:col-span-2">
                  <label className="block text-xs font-semibold text-stone-300 mb-1.5">ملاحظات إضافية</label>
                  <textarea
                    rows={2}
                    className="w-full px-3 py-2 bg-[#172030] text-white border border-stone-800 rounded-xl focus:ring-1 focus:ring-[#D4AF37] focus:border-[#D4AF37] outline-none text-xs resize-none"
                    placeholder="ملاحظات حول طريقة التوصيل، خيارات الإطارات، إلخ..."
                    value={newOrderForm.notes}
                    onChange={(e) => setNewOrderForm({ ...newOrderForm, notes: e.target.value })}
                  />
                </div>
              </div>

              <div className="p-4 border-t border-stone-800 flex justify-end gap-3 bg-[#172030]/50">
                <button
                  type="button"
                  onClick={() => setShowAddOrderModal(false)}
                  className="px-4 py-2 bg-[#172030] hover:bg-[#1f2b40] text-stone-300 rounded-xl text-xs font-bold transition-all"
                >
                  إلغاء
                </button>
                <button
                  type="submit"
                  disabled={isCreatingOrder}
                  className="px-5 py-2 bg-gradient-to-r from-[#BF953F] to-[#AA771C] text-[#111] font-bold rounded-xl hover:brightness-110 active:scale-[0.98] transition-all text-xs disabled:opacity-50 flex items-center gap-2"
                >
                  {isCreatingOrder && <Loader2 className="animate-spin" size={14} />}
                  <span>إنشاء وإرسال الطلب</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit Order Modal */}
      {editingOrder && (
        <div className="fixed inset-0 bg-black/75 flex items-center justify-center p-4 z-50 backdrop-blur-sm">
          <div className="bg-[#121926] border border-[#D4AF37]/20 rounded-3xl w-full max-w-md shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
            <div className="p-4 border-b border-stone-800 flex justify-between items-center bg-[#172030]/50">
              <h3 className="font-bold text-md text-white">
                تعديل تفاصيل الطلب #{editingOrder.scan_id?.substring(0, 6)}
              </h3>
              <button
                onClick={() => setEditingOrder(null)}
                className="text-stone-400 hover:text-white transition-colors"
              >
                <X size={20} />
              </button>
            </div>
            <div className="p-6 flex flex-col gap-4 max-h-[70vh] overflow-y-auto">
              <div>
                <label className="block text-xs font-semibold text-stone-300 mb-1.5">اسم العميل</label>
                <input
                  type="text"
                  className="w-full px-3 py-2 bg-[#172030] text-white border border-stone-800 rounded-xl focus:ring-1 focus:ring-[#D4AF37] focus:border-[#D4AF37] outline-none text-xs"
                  value={editForm.customer_name || ""}
                  onChange={(e) => setEditForm({ ...editForm, customer_name: e.target.value })}
                />
              </div>
              
              <div>
                <label className="block text-xs font-semibold text-stone-300 mb-1.5">رقم الهاتف</label>
                <input
                  type="text"
                  className="w-full px-3 py-2 bg-[#172030] text-white border border-stone-800 rounded-xl focus:ring-1 focus:ring-[#D4AF37] focus:border-[#D4AF37] outline-none text-xs text-left"
                  dir="ltr"
                  value={editForm.customer_phone || ""}
                  onChange={(e) => setEditForm({ ...editForm, customer_phone: e.target.value })}
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-stone-300 mb-1.5">الولاية</label>
                <select
                  className="w-full px-3 py-2 bg-[#172030] text-white border border-stone-800 rounded-xl focus:ring-1 focus:ring-[#D4AF37] focus:border-[#D4AF37] outline-none text-xs cursor-pointer"
                  value={editForm.wilaya || ""}
                  onChange={(e) => setEditForm({ ...editForm, wilaya: e.target.value })}
                >
                  <option value="">اختر الولاية...</option>
                  {ALGERIAN_WILAYAS.map(w => (
                    <option key={w} value={w}>{w}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-stone-300 mb-1.5">العنوان بالتفصيل</label>
                <textarea
                  className="w-full px-3 py-2 bg-[#172030] text-white border border-stone-800 rounded-xl focus:ring-1 focus:ring-[#D4AF37] focus:border-[#D4AF37] outline-none text-xs resize-none"
                  rows={2}
                  value={editForm.delivery_address || ""}
                  onChange={(e) => setEditForm({ ...editForm, delivery_address: e.target.value })}
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-stone-300 mb-1.5">السعر الكلي (د.ج)</label>
                <input
                  type="number"
                  className="w-full px-3 py-2 bg-[#172030] text-white border border-stone-800 rounded-xl focus:ring-1 focus:ring-[#D4AF37] focus:border-[#D4AF37] outline-none text-xs font-sans"
                  value={editForm.total_amount || 0}
                  onChange={(e) => setEditForm({ ...editForm, total_amount: Number(e.target.value) })}
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-stone-300 mb-1.5">ملاحظات</label>
                <textarea
                  className="w-full px-3 py-2 bg-[#172030] text-white border border-stone-800 rounded-xl focus:ring-1 focus:ring-[#D4AF37] focus:border-[#D4AF37] outline-none text-xs resize-none"
                  rows={2}
                  value={editForm.notes || ""}
                  onChange={(e) => setEditForm({ ...editForm, notes: e.target.value })}
                />
              </div>
            </div>
            
            <div className="p-4 border-t border-stone-800 flex justify-end gap-2 bg-[#172030]/50">
              <button
                onClick={() => setEditingOrder(null)}
                className="px-4 py-2 bg-[#172030] hover:bg-[#1f2b40] text-stone-300 rounded-xl text-xs font-bold transition-all"
              >
                إلغاء
              </button>
              <button
                onClick={handleSaveEdit}
                className="px-4 py-2 bg-gradient-to-r from-[#BF953F] to-[#AA771C] text-[#111] font-bold rounded-xl hover:brightness-110 transition-all text-xs flex items-center gap-2"
              >
                <Save size={14} /> 
                <span>حفظ التعديلات</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Waveform Image Modal */}
      {viewingImage && (
        <div className="fixed inset-0 bg-black/90 flex items-center justify-center p-4 z-50 backdrop-blur-sm animate-in fade-in duration-200" onClick={() => setViewingImage(null)}>
          <div className="relative max-w-4xl w-full max-h-[90vh] flex flex-col items-center">
            <button
              onClick={() => setViewingImage(null)}
              className="absolute -top-12 right-0 text-stone-400 hover:text-white transition-colors"
            >
              <X size={32} />
            </button>
            <img
              src={viewingImage}
              alt="Waveform Code Preview"
              className="rounded-2xl shadow-2xl max-w-full max-h-[80vh] object-contain bg-white p-4"
              onClick={(e) => e.stopPropagation()}
            />
            <a
              href={viewingImage}
              download={`waveform_${Date.now()}.png`}
              className="mt-4 bg-gradient-to-r from-[#BF953F] to-[#AA771C] text-[#111] px-6 py-2 rounded-xl font-bold hover:brightness-110 transition-all flex items-center gap-2 text-xs sm:text-sm"
              onClick={(e) => e.stopPropagation()}
            >
              <Download size={16} /> 
              <span>تحميل وحفظ صورة الموجة</span>
            </a>
          </div>
        </div>
      )}

      {/* Hidden Global Audio Player */}
      <audio id="audio-player" onEnded={() => setPlayingAudio(null)} className="hidden" />
    </div>
  );
}
