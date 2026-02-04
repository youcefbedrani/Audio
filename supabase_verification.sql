-- Supabase Database Verification Script
-- Run this in your Supabase SQL Editor to verify all tables and data

-- Test 1: Check if all tables exist
SELECT 
    table_name,
    CASE 
        WHEN table_name IN ('api_frame', 'api_order', 'api_statistic', 'api_audioupload') 
        THEN '✅ EXISTS' 
        ELSE '❌ MISSING' 
    END as status
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE 'api_%'
ORDER BY table_name;

-- Test 2: Check frames table structure and data
SELECT 'FRAMES TABLE TEST' as test_name;
SELECT 
    COUNT(*) as total_frames,
    COUNT(CASE WHEN frame_type = 'wooden' THEN 1 END) as wooden_frames,
    COUNT(CASE WHEN frame_type = 'metal' THEN 1 END) as metal_frames,
    COUNT(CASE WHEN frame_type = 'plastic' THEN 1 END) as plastic_frames,
    COUNT(CASE WHEN frame_type = 'glass' THEN 1 END) as glass_frames,
    COUNT(CASE WHEN is_available = true THEN 1 END) as available_frames,
    COUNT(CASE WHEN title LIKE '%إطار%' THEN 1 END) as arabic_frames
FROM api_frame;

-- Test 3: Check frame details
SELECT 'FRAME DETAILS' as test_name;
SELECT 
    id,
    title,
    frame_type,
    price,
    is_available,
    created_at
FROM api_frame 
ORDER BY id;

-- Test 4: Check statistics table
SELECT 'STATISTICS TABLE TEST' as test_name;
SELECT 
    COUNT(*) as total_stats,
    COUNT(CASE WHEN scans_count > 0 THEN 1 END) as frames_with_scans,
    COUNT(CASE WHEN plays_count > 0 THEN 1 END) as frames_with_plays
FROM api_statistic;

-- Test 5: Check orders table structure
SELECT 'ORDERS TABLE TEST' as test_name;
SELECT 
    COUNT(*) as total_orders,
    COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_orders,
    COUNT(CASE WHEN payment_method = 'COD' THEN 1 END) as cod_orders
FROM api_order;

-- Test 6: Check audio uploads table
SELECT 'AUDIO UPLOADS TABLE TEST' as test_name;
SELECT 
    COUNT(*) as total_uploads,
    AVG(duration) as avg_duration,
    AVG(file_size) as avg_file_size
FROM api_audioupload;

-- Test 7: Check foreign key relationships
SELECT 'FOREIGN KEY RELATIONSHIPS' as test_name;
SELECT 
    'Statistics -> Frames' as relationship,
    COUNT(*) as orphaned_stats
FROM api_statistic s
LEFT JOIN api_frame f ON s.frame_id = f.id
WHERE f.id IS NULL;

SELECT 
    'Orders -> Frames' as relationship,
    COUNT(*) as orphaned_orders
FROM api_order o
LEFT JOIN api_frame f ON o.frame_id = f.id
WHERE f.id IS NULL;

SELECT 
    'Audio Uploads -> Frames' as relationship,
    COUNT(*) as orphaned_uploads
FROM api_audioupload a
LEFT JOIN api_frame f ON a.frame_id = f.id
WHERE f.id IS NULL;

-- Test 8: Check Row Level Security (RLS)
SELECT 'ROW LEVEL SECURITY TEST' as test_name;
SELECT 
    schemaname,
    tablename,
    rowsecurity as rls_enabled
FROM pg_tables 
WHERE tablename LIKE 'api_%'
ORDER BY tablename;

-- Test 9: Check indexes
SELECT 'INDEXES TEST' as test_name;
SELECT 
    indexname,
    tablename,
    indexdef
FROM pg_indexes 
WHERE tablename LIKE 'api_%'
ORDER BY tablename, indexname;

-- Test 10: Insert test (will be rolled back)
BEGIN;
INSERT INTO api_frame (title, description, frame_type, price, is_available) 
VALUES ('Test Frame', 'Test Description', 'wooden', 99.99, true);
SELECT 'INSERT TEST' as test_name, 'SUCCESS' as status;
ROLLBACK;

-- Test 11: Summary report
SELECT 'SUMMARY REPORT' as test_name;
SELECT 
    'Tables' as category,
    COUNT(*) as count
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE 'api_%'

UNION ALL

SELECT 
    'Frames' as category,
    COUNT(*) as count
FROM api_frame

UNION ALL

SELECT 
    'Statistics' as category,
    COUNT(*) as count
FROM api_statistic

UNION ALL

SELECT 
    'Orders' as category,
    COUNT(*) as count
FROM api_order

UNION ALL

SELECT 
    'Audio Uploads' as category,
    COUNT(*) as count
FROM api_audioupload;

-- Final verification
SELECT 'FINAL VERIFICATION' as test_name;
SELECT 
    CASE 
        WHEN (SELECT COUNT(*) FROM api_frame) >= 6 
        AND (SELECT COUNT(*) FROM api_statistic) >= 6
        THEN '✅ DATABASE READY'
        ELSE '❌ DATABASE NOT READY'
    END as status;
