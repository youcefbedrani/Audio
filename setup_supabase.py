#!/usr/bin/env python3
"""
Setup Supabase Database for Audio Frame Art
This script creates the necessary tables in your Supabase database
"""

import requests
import json

# Supabase Configuration
SUPABASE_URL = "https://qksmfogjdurxgzmlcujb.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrc21mb2dqZHVyeGd6bWxjdWpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA0NTg3OTEsImV4cCI6MjA3NjAzNDc5MX0.E1VDpkzcq3AzyPiNZOHU2_5IPyx2k76UdZZiaXg3CVk"

def get_supabase_headers():
    """Get headers for Supabase API calls"""
    return {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

def test_connection():
    """Test connection to Supabase"""
    print("🔍 Testing Supabase connection...")
    try:
        headers = get_supabase_headers()
        response = requests.get(f"{SUPABASE_URL}/rest/v1/", headers=headers)
        if response.status_code == 200:
            print("✅ Connected to Supabase successfully!")
            return True
        else:
            print(f"❌ Connection failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def create_orders_table():
    """Create the api_order table"""
    print("\n📋 Creating api_order table...")
    
    # SQL to create the table
    sql = """
    CREATE TABLE IF NOT EXISTS api_order (
        id BIGSERIAL PRIMARY KEY,
        customer_name TEXT NOT NULL,
        customer_phone TEXT NOT NULL,
        customer_email TEXT DEFAULT '',
        delivery_address TEXT NOT NULL,
        city TEXT NOT NULL,
        postal_code TEXT DEFAULT '',
        wilaya TEXT DEFAULT '',
        baladya TEXT DEFAULT '',
        frame_id INTEGER NOT NULL,
        audio_file_url TEXT,
        status TEXT DEFAULT 'pending',
        payment_method TEXT DEFAULT 'COD',
        total_amount DECIMAL(10,2) NOT NULL,
        notes TEXT DEFAULT '',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- Enable RLS
    ALTER TABLE api_order ENABLE ROW LEVEL SECURITY;
    
    -- Allow public access for demo (in production, use proper user-based policies)
    DROP POLICY IF EXISTS "Allow public access to api_order" ON api_order;
    CREATE POLICY "Allow public access to api_order" ON api_order
        FOR ALL USING (true);
    
    -- Create indexes for better performance
    CREATE INDEX IF NOT EXISTS idx_api_order_frame_id ON api_order(frame_id);
    CREATE INDEX IF NOT EXISTS idx_api_order_created_at ON api_order(created_at);
    CREATE INDEX IF NOT EXISTS idx_api_order_status ON api_order(status);
    """
    
    try:
        # Use Supabase's SQL execution endpoint
        headers = get_supabase_headers()
        headers["Content-Type"] = "application/vnd.pgrst.object+json"
        
        # Execute SQL
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/rpc/exec_sql",
            headers=headers,
            json={"sql": sql}
        )
        
        if response.status_code == 200:
            print("✅ api_order table created successfully!")
            return True
        else:
            print(f"❌ Failed to create table: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error creating table: {e}")
        return False

def test_table_access():
    """Test if we can access the table"""
    print("\n🔍 Testing table access...")
    try:
        headers = get_supabase_headers()
        response = requests.get(f"{SUPABASE_URL}/rest/v1/api_order", headers=headers)
        
        if response.status_code == 200:
            print("✅ Table access successful!")
            orders = response.json()
            print(f"   Found {len(orders)} existing orders")
            return True
        else:
            print(f"❌ Table access failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error accessing table: {e}")
        return False

def create_sample_order():
    """Create a sample order to test the setup"""
    print("\n📝 Creating sample order...")
    try:
        headers = get_supabase_headers()
        
        sample_order = {
            "customer_name": "Test User Setup",
            "customer_phone": "0555123456",
            "customer_email": "test@example.com",
            "delivery_address": "Test Address, Algiers",
            "city": "Algiers",
            "wilaya": "الجزائر",
            "baladya": "الجزائر",
            "frame_id": 1,
            "audio_file_url": "https://example.com/test-audio.mp3",
            "status": "pending",
            "payment_method": "COD",
            "total_amount": 150.00,
            "notes": "Test order created during setup"
        }
        
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/api_order",
            headers=headers,
            json=sample_order
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            print("✅ Sample order created successfully!")
            print(f"   Order ID: {result[0]['id'] if isinstance(result, list) else result.get('id')}")
            return True
        else:
            print(f"❌ Failed to create sample order: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error creating sample order: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Supabase Database for Audio Frame Art")
    print("=" * 60)
    
    # Test connection
    if not test_connection():
        print("\n❌ Cannot connect to Supabase. Please check your credentials.")
        return
    
    # Create table
    if not create_orders_table():
        print("\n❌ Failed to create table. You may need to run the SQL manually in Supabase dashboard.")
        print("\n📋 Manual Setup Instructions:")
        print("1. Go to: https://supabase.com/dashboard/project/qksmfogjdurxgzmlcujb")
        print("2. Go to SQL Editor")
        print("3. Run this SQL:")
        print("""
        CREATE TABLE IF NOT EXISTS api_order (
            id BIGSERIAL PRIMARY KEY,
            customer_name TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            customer_email TEXT DEFAULT '',
            delivery_address TEXT NOT NULL,
            city TEXT NOT NULL,
            postal_code TEXT DEFAULT '',
            wilaya TEXT DEFAULT '',
            baladya TEXT DEFAULT '',
            frame_id INTEGER NOT NULL,
            audio_file_url TEXT,
            status TEXT DEFAULT 'pending',
            payment_method TEXT DEFAULT 'COD',
            total_amount DECIMAL(10,2) NOT NULL,
            notes TEXT DEFAULT '',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        ALTER TABLE api_order ENABLE ROW LEVEL SECURITY;
        CREATE POLICY "Allow public access to api_order" ON api_order FOR ALL USING (true);
        """)
        return
    
    # Test table access
    if not test_table_access():
        print("\n❌ Cannot access table. Please check table permissions.")
        return
    
    # Create sample order
    create_sample_order()
    
    print("\n" + "=" * 60)
    print("🎉 Supabase setup completed!")
    print("\n📊 Next steps:")
    print("1. Start your API: docker-compose up -d")
    print("2. Test order creation")
    print("3. Check your Supabase dashboard to see orders")
    print(f"\n🔗 Supabase Dashboard: https://supabase.com/dashboard/project/qksmfogjdurxgzmlcujb")

if __name__ == "__main__":
    main()
