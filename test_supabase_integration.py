#!/usr/bin/env python3
"""
Test Supabase Integration for Audio Frame Art
"""

import requests
import json
import time

# API Configuration
API_BASE_URL = "http://localhost:8001"
SUPABASE_URL = "https://qksmfogjdurxgzmlcujb.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrc21mb2dqZHVyeGd6bWxjdWpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA0NTg3OTEsImV4cCI6MjA3NjAzNDc5MX0.E1VDpkzcq3AzyPiNZOHU2_5IPyx2k76UdZZiaXg3CVk"

def test_api_health():
    """Test API health"""
    print("🔍 Testing API Health...")
    try:
        response = requests.get(f"{API_BASE_URL}/health/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Health: {data['status']}")
            print(f"   Supabase Connected: {data.get('supabase_connected', False)}")
            print(f"   Cloudinary Configured: {data.get('cloudinary_configured', False)}")
            return True
        else:
            print(f"❌ API Health failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Health error: {e}")
        return False

def test_frames_api():
    """Test frames API"""
    print("\n🔍 Testing Frames API...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/frames/")
        if response.status_code == 200:
            frames = response.json()
            print(f"✅ Frames API: Found {len(frames)} frames")
            for frame in frames[:2]:  # Show first 2 frames
                print(f"   - {frame['title']} (${frame['price']})")
            return True
        else:
            print(f"❌ Frames API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frames API error: {e}")
        return False

def test_order_creation():
    """Test order creation with Supabase"""
    print("\n🔍 Testing Order Creation...")
    try:
        # Test order data
        order_data = {
            "customer_name": "Test User Supabase",
            "customer_phone": "0555123456",
            "delivery_address": "Test Address, Algiers",
            "city": "Algiers",
            "wilaya": "الجزائر",
            "baladya": "الجزائر",
            "frame": "1",
            "payment_method": "COD"
        }
        
        response = requests.post(f"{API_BASE_URL}/api/orders/", data=order_data)
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Order Created Successfully!")
            print(f"   Order ID: {data['id']}")
            print(f"   Message: {data['message']}")
            if 'supabase_id' in data:
                print(f"   Supabase ID: {data['supabase_id']}")
            return data['id']
        else:
            print(f"❌ Order Creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Order Creation error: {e}")
        return None

def test_orders_list():
    """Test orders list from Supabase"""
    print("\n🔍 Testing Orders List...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/orders/")
        if response.status_code == 200:
            orders = response.json()
            print(f"✅ Orders List: Found {len(orders)} orders")
            for order in orders[-3:]:  # Show last 3 orders
                print(f"   - Order {order['id']}: {order['customer_name']} - {order['frame_title']}")
            return True
        else:
            print(f"❌ Orders List failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Orders List error: {e}")
        return False

def test_qr_scan():
    """Test QR code scanning"""
    print("\n🔍 Testing QR Code Scan...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/scan/1/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ QR Scan: {data['message']}")
            print(f"   Frame: {data['frame_title']}")
            print(f"   Audio URL: {data['audio_url']}")
            return True
        else:
            print(f"❌ QR Scan failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ QR Scan error: {e}")
        return False

def test_statistics():
    """Test statistics API"""
    print("\n🔍 Testing Statistics...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/statistics/")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Statistics:")
            print(f"   Total Orders: {stats['total_orders']}")
            print(f"   Total Frames: {stats['total_frames']}")
            print(f"   Pending Orders: {stats['pending_orders']}")
            return True
        else:
            print(f"❌ Statistics failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Statistics error: {e}")
        return False

def test_direct_supabase():
    """Test direct Supabase connection"""
    print("\n🔍 Testing Direct Supabase Connection...")
    try:
        headers = {
            "apikey": SUPABASE_ANON_KEY,
            "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
            "Content-Type": "application/json"
        }
        
        # Test frames table
        response = requests.get(f"{SUPABASE_URL}/rest/v1/frames", headers=headers)
        if response.status_code == 200:
            frames = response.json()
            print(f"✅ Direct Supabase: Found {len(frames)} frames in database")
        else:
            print(f"❌ Direct Supabase frames failed: {response.status_code}")
        
        # Test orders table
        response = requests.get(f"{SUPABASE_URL}/rest/v1/orders", headers=headers)
        if response.status_code == 200:
            orders = response.json()
            print(f"✅ Direct Supabase: Found {len(orders)} orders in database")
            if orders:
                latest_order = orders[-1]
                print(f"   Latest Order: {latest_order['customer_name']} - {latest_order['frame_title']}")
        else:
            print(f"❌ Direct Supabase orders failed: {response.status_code}")
            print(f"   Response: {response.text}")
        
        return True
    except Exception as e:
        print(f"❌ Direct Supabase error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Supabase Integration Test Suite")
    print("=" * 50)
    
    # Wait for API to be ready
    print("⏳ Waiting for API to be ready...")
    time.sleep(3)
    
    # Run tests
    tests = [
        test_api_health,
        test_frames_api,
        test_order_creation,
        test_orders_list,
        test_qr_scan,
        test_statistics,
        test_direct_supabase
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Supabase integration is working!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    print("\n🔗 Useful Links:")
    print(f"   API Health: {API_BASE_URL}/health/")
    print(f"   Orders API: {API_BASE_URL}/api/orders/")
    print(f"   Supabase Dashboard: https://supabase.com/dashboard/project/qksmfogjdurxgzmlcujb")

if __name__ == "__main__":
    main()
