import axios from "axios";
import type { Order } from "./types";

export interface Settings {
  fb_pixel_id: string;
  tiktok_pixel_id: string;
}

const getApiUrl = () => {
  // Always use relative path in the browser to work with Nginx proxy (SSL or not)
  if (typeof window !== 'undefined') {
    return "/api";
  }

  // Try environment variable for server-side (Node.js context)
  const envUrl = process.env.NEXT_PUBLIC_API_URL;
  if (envUrl && !envUrl.includes('localhost')) {
    return envUrl.endsWith('/api') ? envUrl : `${envUrl}/api`;
  }

  // Fallback for local development if not proxied
  return "http://localhost:8001/api";
};

const API_URL = getApiUrl();

export interface CreateOrderResponse {
  success: boolean;
  order_id?: string;
  message?: string;
  qr_code_url?: string;
  waveform_url?: string;
}

export const createOrder = async (
  orderData: Order,
  audioBlob: Blob
): Promise<CreateOrderResponse> => {
  try {
    const formData = new FormData();

    // Append order details
    formData.append("customer_name", orderData.customer_name);
    formData.append("customer_phone", orderData.customer_phone);
    formData.append("wilaya", orderData.wilaya);
    formData.append("address", orderData.delivery_address);
    formData.append("baladiya", orderData.baladya || orderData.wilaya);
    formData.append("city", orderData.baladya || orderData.wilaya); // Required by backend
    formData.append("frame_id", String(orderData.frame_id));

    // Append audio file
    formData.append("audio_file", audioBlob, "recording.webm");

    const response = await axios.post(`${API_URL}/orders/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return response.data;
  } catch (error) {
    console.error("Error creating order:", error);
    throw error;
  }
};

// Pagination Response Type
export interface PaginatedOrders {
  orders: Order[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

export const getOrders = async (
  page = 1,
  limit = 30,
  search?: string,
  status?: string
): Promise<PaginatedOrders> => {
  try {
    const response = await axios.get(`${API_URL}/orders/`, {
      params: { page, limit, search, status }
    });
    // Handle both old array format (fallback) and new paginated format
    if (Array.isArray(response.data)) {
      return {
        orders: response.data,
        total: response.data.length,
        page: 1,
        limit: response.data.length,
        total_pages: 1
      };
    }
    return response.data;
  } catch (error) {
    console.error("Error fetching orders:", error);
    throw error;
  }
};

export const updateOrderStatus = async (
  orderId: string | number,
  status: string,
  confirmationAgent?: string
) => {
  try {
    const response = await axios.put(`${API_URL}/orders/${orderId}/status`, {
      status,
      confirmation_agent: confirmationAgent,
    });
    return response.data;
  } catch (error) {
    console.error("Error updating order status:", error);
    throw error;
  }
};

export const updateOrderDetails = async (orderId: string | number, updates: any) => {
  try {
    const response = await axios.put(`${API_URL}/orders/${orderId}`, updates);
    return response.data;
  } catch (error) {
    console.error("Error updating order details:", error);
    throw error;
  }
};

export const deleteOrder = async (orderId: string | number) => {
  try {
    const response = await axios.delete(`${API_URL}/orders/${orderId}`);
    return response.data;
  } catch (error) {
    console.error("Error deleting order:", error);
    throw error;
  }
};

export const getConfirmationAgents = async (): Promise<string[]> => {
  try {
    const response = await axios.get(`${API_URL}/confirmation-agents/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching agents:", error);
    return [];
  }
};

export const addConfirmationAgent = async (name: string) => {
  try {
    const response = await axios.post(`${API_URL}/confirmation-agents/`, { name });
    return response.data;
  } catch (error) {
    console.error("Error adding agent:", error);
    throw error;
  }
};

export const deleteConfirmationAgent = async (name: string) => {
  try {
    const response = await axios.delete(`${API_URL}/confirmation-agents/${encodeURIComponent(name)}`);
    return response.data;
  } catch (error) {
    console.error("Error deleting agent:", error);
    throw error;
  }
};

export const getSettings = async (): Promise<Settings> => {
  try {
    const response = await axios.get(`${API_URL}/settings/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching settings:", error);
    return { fb_pixel_id: "", tiktok_pixel_id: "" };
  }
};

export const updateSettings = async (settings: Settings) => {
  try {
    const response = await axios.post(`${API_URL}/settings/`, settings);
    return response.data;
  } catch (error) {
    console.error("Error updating settings:", error);
    throw error;
  }


};

export const getAdminStats = async (): Promise<import("./types").AdminStatsData> => {
  try {
    const response = await axios.get(`${API_URL}/admin/stats/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching admin stats:", error);
    throw error;
  }
};