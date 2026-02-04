-- update_schema.sql
-- Run this in your Supabase SQL Editor to update the database schema

-- 1. Create confirmation_agents table
CREATE TABLE IF NOT EXISTS confirmation_agents (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Enable RLS for confirmation_agents
ALTER TABLE confirmation_agents ENABLE ROW LEVEL SECURITY;

-- 3. Allow public access to confirmation_agents
DROP POLICY IF EXISTS "Allow public access to confirmation_agents" ON confirmation_agents;
CREATE POLICY "Allow public access to confirmation_agents" ON confirmation_agents
    FOR ALL USING (true);

-- 4. Add confirmation_agent column to api_order
ALTER TABLE api_order ADD COLUMN IF NOT EXISTS confirmation_agent TEXT;

-- 5. Add confirmation_agent column to orders table (if it exists)
DO $$
BEGIN
    IF EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'orders') THEN
        ALTER TABLE orders ADD COLUMN IF NOT EXISTS confirmation_agent TEXT;
    END IF;
END $$;
