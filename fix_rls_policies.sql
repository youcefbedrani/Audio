-- Fix RLS policies for api_order table to allow anonymous inserts
-- This allows orders to be created without authentication

-- Drop existing policies
DROP POLICY IF EXISTS "Users can view their own orders" ON api_order;
DROP POLICY IF EXISTS "Users can insert their own orders" ON api_order;
DROP POLICY IF EXISTS "Users can update their own orders" ON api_order;

-- Create new policies that allow anonymous access
CREATE POLICY "Allow anonymous inserts" ON api_order FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow anonymous selects" ON api_order FOR SELECT USING (true);
CREATE POLICY "Allow anonymous updates" ON api_order FOR UPDATE USING (true);

-- Also fix api_frame table policies
DROP POLICY IF EXISTS "Users can view all frames" ON api_frame;
DROP POLICY IF EXISTS "Users can insert their own frames" ON api_frame;
DROP POLICY IF EXISTS "Users can update their own frames" ON api_frame;

CREATE POLICY "Allow anonymous frame access" ON api_frame FOR ALL USING (true);

-- Fix api_statistic table policies
DROP POLICY IF EXISTS "Users can view all statistics" ON api_statistic;
DROP POLICY IF EXISTS "Users can insert statistics" ON api_statistic;
DROP POLICY IF EXISTS "Users can update statistics" ON api_statistic;

CREATE POLICY "Allow anonymous statistic access" ON api_statistic FOR ALL USING (true);

-- Fix api_audioupload table policies
DROP POLICY IF EXISTS "Users can view their own audio uploads" ON api_audioupload;
DROP POLICY IF EXISTS "Users can insert their own audio uploads" ON api_audioupload;
DROP POLICY IF EXISTS "Users can update their own audio uploads" ON api_audioupload;

CREATE POLICY "Allow anonymous audio upload access" ON api_audioupload FOR ALL USING (true);

