export interface Product {
    id: string;
    name: string;
    description: string;
    price: number;
    currency: string;
    images: string[];
    dimensions: string;
    colors: string[];
}

export interface AudioData {
    blob: Blob;
    url: string;
    duration: number;
}

export interface Order {
    id: string | number;
    scan_id?: string;
    customer_name: string;
    customer_phone: string;
    customer_email?: string;
    delivery_address: string;
    wilaya: string;
    baladya?: string; // Optional field in backend
    frame_id: string | number;
    frame_title?: string;
    frame_type?: string;
    audio_file_url?: string;
    qr_code_url?: string;
    qr_code_data?: string;
    status: 'pending' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled' | 'no_response';
    confirmation_agent?: string;
    total_amount: number;
    notes?: string;
    created_at?: string;
}

export interface AdminStatsData {
    total_orders: number;
    confirmed_orders: number;
    shipped_orders: number;
    total_revenue: number;
    agent_stats: Record<string, number>;
}

export const WILAYAS = [
    "Adrar", "Chlef", "Laghouat", "Oum El Bouaghi", "Batna", "Béjaïa", "Biskra", "Béchar",
    "Blida", "Bouira", "Tamanrasset", "Tébessa", "Tlemcen", "Tiaret", "Tizi Ouzou", "Algiers",
    "Djelfa", "Jijel", "Sétif", "Saïda", "Skikda", "Sidi Bel Abbès", "Annaba", "Guelma",
    "Constantine", "Médéa", "Mostaganem", "M'Sila", "Mascara", "Ouargla", "Oran", "El Bayadh",
    "Illizi", "Bordj Bou Arréridj", "Boumerdès", "El Tarf", "Tindouf", "Tissemsilt", "El Oued",
    "Khenchela", "Souk Ahras", "Tipaza", "Mila", "Aïn Defla", "Naâma", "Aïn Témouchent",
    "Ghardaïa", "Relizane", "Timimoun", "Bordj Badji Mokhtar", "Ouled Djellal", "Béni Abbès",
    "In Salah", "In Guezzam", "Touggourt", "Djanet", "El M'Ghair", "El Meniaa"
];
