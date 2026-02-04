#!/usr/bin/env python3
"""
Update Supabase Database Schema
Add confirmation_agents table and update api_order table
"""

import requests
import json
import sys

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

def update_schema():
    """Execute SQL to update schema"""
    print("📋 Updating database schema...")
    
    sql = """
    -- Create confirmation_agents table
    CREATE TABLE IF NOT EXISTS confirmation_agents (
        id SERIAL PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Enable RLS for confirmation_agents
    ALTER TABLE confirmation_agents ENABLE ROW LEVEL SECURITY;

    -- Allow public access to confirmation_agents
    DROP POLICY IF EXISTS "Allow public access to confirmation_agents" ON confirmation_agents;
    CREATE POLICY "Allow public access to confirmation_agents" ON confirmation_agents
        FOR ALL USING (true);

    -- Add confirmation_agent column to api_order
    ALTER TABLE api_order ADD COLUMN IF NOT EXISTS confirmation_agent TEXT;
    
    -- Add confirmation_agent column to orders table if it exists (for compatibility)
    DO $$
    BEGIN
        IF EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'orders') THEN
            ALTER TABLE orders ADD COLUMN IF NOT EXISTS confirmation_agent TEXT;
        END IF;
    END $$;
    """
    
    try:
        # Use Supabase's SQL execution endpoint
        headers = get_supabase_headers()
        # headers["Content-Type"] = "application/vnd.pgrst.object+json" # This might be correct for RPC?
        # Actually setup_supabase.py used this, let's stick to it but api might typically be application/json
        
        # NOTE: rpc/exec_sql implies a stored procedure named exec_sql exists. 
        # If setup_supabase.py used it successfully, it must exist.
        
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/rpc/exec_sql",
            headers=headers,
            json={"sql": sql}
        )
        
        if response.status_code == 200:
            print("✅ Schema updated successfully!")
            return True
        else:
            print(f"❌ Failed to update schema: {response.status_code}")
            print(f"   Response: {response.text}")
            # If exec_sql is not available, we can't do much via script.
            if response.status_code == 404:
                print("   The 'exec_sql' RPC function was not found. Please run screen SQL manually.")
            return False
            
    except Exception as e:
        print(f"❌ Error updating schema: {e}")
        return False

if __name__ == "__main__":
    success = update_schema()
    if not success:
        sys.exit(1)
