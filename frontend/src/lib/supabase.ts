import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Database types
export interface Database {
  public: {
    Tables: {
      api_frame: {
        Row: {
          id: number
          title: string
          description: string | null
          frame_type: 'wooden' | 'metal' | 'plastic' | 'glass'
          image: string | null
          qr_code: string | null
          audio_file: string | null
          owner_id: number | null
          price: number
          is_available: boolean
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: number
          title: string
          description?: string | null
          frame_type?: 'wooden' | 'metal' | 'plastic' | 'glass'
          image?: string | null
          qr_code?: string | null
          audio_file?: string | null
          owner_id?: number | null
          price?: number
          is_available?: boolean
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: number
          title?: string
          description?: string | null
          frame_type?: 'wooden' | 'metal' | 'plastic' | 'glass'
          image?: string | null
          qr_code?: string | null
          audio_file?: string | null
          owner_id?: number | null
          price?: number
          is_available?: boolean
          created_at?: string
          updated_at?: string
        }
      }
      api_order: {
        Row: {
          id: number
          user_id: number | null
          frame_id: number
          customer_name: string
          customer_phone: string
          customer_email: string | null
          delivery_address: string
          city: string
          postal_code: string
          status: 'pending' | 'confirmed' | 'processing' | 'shipped' | 'delivered' | 'cancelled'
          payment_method: 'COD' | 'online'
          total_amount: number
          notes: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: number
          user_id?: number | null
          frame_id: number
          customer_name: string
          customer_phone: string
          customer_email?: string | null
          delivery_address: string
          city: string
          postal_code: string
          status?: 'pending' | 'confirmed' | 'processing' | 'shipped' | 'delivered' | 'cancelled'
          payment_method?: 'COD' | 'online'
          total_amount: number
          notes?: string | null
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: number
          user_id?: number | null
          frame_id?: number
          customer_name?: string
          customer_phone?: string
          customer_email?: string | null
          delivery_address?: string
          city?: string
          postal_code?: string
          status?: 'pending' | 'confirmed' | 'processing' | 'shipped' | 'delivered' | 'cancelled'
          payment_method?: 'COD' | 'online'
          total_amount?: number
          notes?: string | null
          created_at?: string
          updated_at?: string
        }
      }
      api_statistic: {
        Row: {
          id: number
          frame_id: number
          scans_count: number
          plays_count: number
          last_scan: string | null
          last_play: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: number
          frame_id: number
          scans_count?: number
          plays_count?: number
          last_scan?: string | null
          last_play?: string | null
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: number
          frame_id?: number
          scans_count?: number
          plays_count?: number
          last_scan?: string | null
          last_play?: string | null
          created_at?: string
          updated_at?: string
        }
      }
    }
  }
}
