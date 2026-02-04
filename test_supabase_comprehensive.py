#!/usr/bin/env python3
"""
Comprehensive Supabase Test Script
Tests all tables, data, and functionality.
"""
import os
import sys
import json
from decouple import config

# Add the backend directory to Python path
sys.path.append('backend')

def test_supabase_connection():
    """Test basic Supabase connection."""
    print("🔗 Testing Supabase Connection...")
    try:
        from supabase import create_client
        
        supabase_url = config('SUPABASE_URL')
        supabase_key = config('SUPABASE_ANON_KEY')
        
        print(f"   URL: {supabase_url}")
        print(f"   Key: {supabase_key[:20]}...")
        
        supabase = create_client(supabase_url, supabase_key)
        print("   ✅ Supabase client created successfully")
        return supabase
        
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return None

def test_table_exists(supabase, table_name):
    """Test if a table exists and is accessible."""
    print(f"📊 Testing table: {table_name}")
    try:
        result = supabase.table(table_name).select('*').limit(1).execute()
        print(f"   ✅ Table '{table_name}' exists and accessible")
        return True
    except Exception as e:
        print(f"   ❌ Table '{table_name}' error: {e}")
        return False

def test_frames_table(supabase):
    """Test frames table structure and data."""
    print("\n🖼️  Testing Frames Table...")
    try:
        # Test basic select
        result = supabase.table('api_frame').select('*').execute()
        frames = result.data
        
        print(f"   📦 Found {len(frames)} frames")
        
        if len(frames) > 0:
            frame = frames[0]
            required_fields = ['id', 'title', 'description', 'frame_type', 'price', 'is_available']
            
            print("   🔍 Checking required fields:")
            for field in required_fields:
                if field in frame:
                    print(f"      ✅ {field}: {frame[field]}")
                else:
                    print(f"      ❌ Missing field: {field}")
            
            # Test frame types
            frame_types = ['wooden', 'metal', 'plastic', 'glass']
            print("   🎨 Testing frame types:")
            for frame_type in frame_types:
                count = len([f for f in frames if f.get('frame_type') == frame_type])
                print(f"      {frame_type}: {count} frames")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Frames table error: {e}")
        return False

def test_orders_table(supabase):
    """Test orders table structure."""
    print("\n📋 Testing Orders Table...")
    try:
        result = supabase.table('api_order').select('*').execute()
        orders = result.data
        
        print(f"   📦 Found {len(orders)} orders")
        
        if len(orders) > 0:
            order = orders[0]
            required_fields = ['id', 'customer_name', 'customer_phone', 'delivery_address', 'city', 'status', 'payment_method', 'total_amount']
            
            print("   🔍 Checking required fields:")
            for field in required_fields:
                if field in order:
                    print(f"      ✅ {field}: {order[field]}")
                else:
                    print(f"      ❌ Missing field: {field}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Orders table error: {e}")
        return False

def test_statistics_table(supabase):
    """Test statistics table structure."""
    print("\n📈 Testing Statistics Table...")
    try:
        result = supabase.table('api_statistic').select('*').execute()
        stats = result.data
        
        print(f"   📦 Found {len(stats)} statistics records")
        
        if len(stats) > 0:
            stat = stats[0]
            required_fields = ['id', 'frame_id', 'scans_count', 'plays_count']
            
            print("   🔍 Checking required fields:")
            for field in required_fields:
                if field in stat:
                    print(f"      ✅ {field}: {stat[field]}")
                else:
                    print(f"      ❌ Missing field: {field}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Statistics table error: {e}")
        return False

def test_audio_uploads_table(supabase):
    """Test audio uploads table structure."""
    print("\n🎵 Testing Audio Uploads Table...")
    try:
        result = supabase.table('api_audioupload').select('*').execute()
        uploads = result.data
        
        print(f"   📦 Found {len(uploads)} audio uploads")
        
        if len(uploads) > 0:
            upload = uploads[0]
            required_fields = ['id', 'frame_id', 'audio_file', 'duration', 'file_size']
            
            print("   🔍 Checking required fields:")
            for field in required_fields:
                if field in upload:
                    print(f"      ✅ {field}: {upload[field]}")
                else:
                    print(f"      ❌ Missing field: {field}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Audio uploads table error: {e}")
        return False

def test_sample_data(supabase):
    """Test if sample data is present."""
    print("\n📊 Testing Sample Data...")
    try:
        # Check frames
        frames_result = supabase.table('api_frame').select('*').execute()
        frames = frames_result.data
        
        print(f"   🖼️  Frames: {len(frames)}")
        
        # Check for Arabic frames
        arabic_frames = [f for f in frames if 'إطار' in f.get('title', '')]
        print(f"   🇸🇦 Arabic frames: {len(arabic_frames)}")
        
        # Check frame types
        frame_types = {}
        for frame in frames:
            frame_type = frame.get('frame_type', 'unknown')
            frame_types[frame_type] = frame_types.get(frame_type, 0) + 1
        
        print("   📊 Frame type distribution:")
        for frame_type, count in frame_types.items():
            print(f"      {frame_type}: {count}")
        
        # Check statistics
        stats_result = supabase.table('api_statistic').select('*').execute()
        stats = stats_result.data
        print(f"   📈 Statistics records: {len(stats)}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Sample data test error: {e}")
        return False

def test_insert_capability(supabase):
    """Test if we can insert data."""
    print("\n➕ Testing Insert Capability...")
    try:
        # Try to insert a test frame
        test_frame = {
            'title': 'Test Frame',
            'description': 'Test description',
            'frame_type': 'wooden',
            'price': 100.00,
            'is_available': True
        }
        
        result = supabase.table('api_frame').insert(test_frame).execute()
        
        if result.data:
            print("   ✅ Insert test successful")
            
            # Clean up - delete the test frame
            frame_id = result.data[0]['id']
            supabase.table('api_frame').delete().eq('id', frame_id).execute()
            print("   🧹 Test frame cleaned up")
            
            return True
        else:
            print("   ❌ Insert test failed - no data returned")
            return False
            
    except Exception as e:
        print(f"   ❌ Insert test error: {e}")
        return False

def test_environment_variables():
    """Test all required environment variables."""
    print("🔧 Testing Environment Variables...")
    
    required_vars = {
        'SUPABASE_URL': 'https://qksmfogjdurxgzmlcujb.supabase.co',
        'SUPABASE_ANON_KEY': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
        'DB_HOST': 'db.qksmfogjdurxgzmlcujb.supabase.co',
        'DB_NAME': 'postgres',
        'DB_USER': 'postgres',
        'DB_PASSWORD': 'your-supabase-db-password'
    }
    
    all_good = True
    for var, expected_start in required_vars.items():
        try:
            value = config(var)
            if not value:
                print(f"   ❌ {var}: Not set")
                all_good = False
            elif var == 'DB_PASSWORD' and value == 'your-supabase-db-password':
                print(f"   ⚠️  {var}: Please update with your actual password")
                all_good = False
            elif expected_start and not value.startswith(expected_start):
                print(f"   ⚠️  {var}: Unexpected value (expected to start with '{expected_start}')")
            else:
                print(f"   ✅ {var}: {value[:30]}{'...' if len(value) > 30 else ''}")
        except:
            print(f"   ❌ {var}: Not found")
            all_good = False
    
    return all_good

def main():
    """Run all tests."""
    print("🚀 SUPABASE COMPREHENSIVE TEST")
    print("=" * 50)
    
    # Test environment variables
    env_ok = test_environment_variables()
    print()
    
    if not env_ok:
        print("❌ Environment variables not properly configured!")
        print("Please update your .env file with correct values.")
        return
    
    # Test Supabase connection
    supabase = test_supabase_connection()
    if not supabase:
        print("❌ Cannot connect to Supabase!")
        return
    
    # Test all tables
    tables = ['api_frame', 'api_order', 'api_statistic', 'api_audioupload']
    table_results = []
    
    for table in tables:
        table_results.append(test_table_exists(supabase, table))
    
    print()
    
    # Test specific table functionality
    frames_ok = test_frames_table(supabase)
    orders_ok = test_orders_table(supabase)
    stats_ok = test_statistics_table(supabase)
    audio_ok = test_audio_uploads_table(supabase)
    
    # Test sample data
    sample_ok = test_sample_data(supabase)
    
    # Test insert capability
    insert_ok = test_insert_capability(supabase)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    tests = [
        ("Environment Variables", env_ok),
        ("Supabase Connection", supabase is not None),
        ("All Tables Exist", all(table_results)),
        ("Frames Table", frames_ok),
        ("Orders Table", orders_ok),
        ("Statistics Table", stats_ok),
        ("Audio Uploads Table", audio_ok),
        ("Sample Data", sample_ok),
        ("Insert Capability", insert_ok)
    ]
    
    passed = 0
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:25} {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n🎉 ALL TESTS PASSED! Supabase is ready to use!")
        print("\n📋 Next steps:")
        print("1. Start your application: docker-compose -f docker-compose.supabase.yml up")
        print("2. Run migrations: docker-compose -f docker-compose.supabase.yml exec api python manage.py migrate")
        print("3. Create admin user: docker-compose -f docker-compose.supabase.yml exec api python manage.py createsuperuser")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
        print("\n🔧 Common fixes:")
        print("- Update your .env file with correct Supabase credentials")
        print("- Run the SQL schema in Supabase SQL Editor")
        print("- Check your Supabase project settings")

if __name__ == "__main__":
    main()
