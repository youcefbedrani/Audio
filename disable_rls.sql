-- Temporarily disable RLS for api_order table to allow anonymous inserts
ALTER TABLE api_order DISABLE ROW LEVEL SECURITY;

-- Also disable RLS for other tables to ensure everything works
ALTER TABLE api_frame DISABLE ROW LEVEL SECURITY;
ALTER TABLE api_statistic DISABLE ROW LEVEL SECURITY;
ALTER TABLE api_audioupload DISABLE ROW LEVEL SECURITY;

