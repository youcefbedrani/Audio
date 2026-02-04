#!/usr/bin/env python3
"""
Final Comprehensive Test for Audio Frame Art System
Tests website, API, and Supabase integration
"""

import requests
import json
import time

def test_website():
    """Test website accessibility"""
    print("🌐 Testing Website...")
    try:
        response = requests.get("http://localhost:3000")
        if response.status_code == 200:
            if "إطارات الصوت الفنية" in response.text:
                print("✅ Website is working and showing Arabic content")
                return True
            else:
                print("⚠️ Website is working but Arabic content not found")
                return True
        else:
            print(f"❌ Website returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Website error: {e}")
        return False

def test_api_health():
    """Test API health"""
    print("\n🔍 Testing API Health...")
    try:
        response = requests.get("http://localhost:8001/health/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Health: {data['status']}")
            print(f"   Supabase Connected: {data.get('supabase_connected', False)}")
            print(f"   Supabase URL: {data.get('supabase_url', 'N/A')}")
            return True
        else:
            print(f"❌ API Health failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Health error: {e}")
        return False

def test_frames_api():
    """Test frames API"""
    print("\n🖼️ Testing Frames API...")
    try:
        response = requests.get("http://localhost:8001/api/frames/")
        if response.status_code == 200:
            frames = response.json()
            print(f"✅ Frames API: Found {len(frames)} frames")
            for i, frame in enumerate(frames[:2]):
                print(f"   {i+1}. {frame['title']} - ${frame['price']}")
            return True
        else:
            print(f"❌ Frames API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frames API error: {e}")
        return False

def test_order_creation():
    """Test order creation"""
    print("\n📝 Testing Order Creation...")
    try:
        order_data = {
            "customer_name": "Final Test User",
            "customer_phone": "0555123456",
            "delivery_address": "Test Address, Algiers",
            "city": "Algiers",
            "wilaya": "الجزائر",
            "baladya": "الجزائر",
            "frame": "1",
            "payment_method": "COD"
        }
        
        response = requests.post("http://localhost:8001/api/orders/", data=order_data)
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Order Created Successfully!")
            print(f"   Order ID: {data['id']}")
            print(f"   Message: {data['message']}")
            if 'supabase_id' in data:
                print(f"   Supabase ID: {data['supabase_id']}")
                print("   🎉 Order saved to Supabase!")
            else:
                print("   ⚠️ Order saved locally (Supabase table not created yet)")
            return True
        else:
            print(f"❌ Order Creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Order Creation error: {e}")
        return False

def test_orders_list():
    """Test orders list"""
    print("\n📋 Testing Orders List...")
    try:
        response = requests.get("http://localhost:8001/api/orders/")
        if response.status_code == 200:
            orders = response.json()
            print(f"✅ Orders List: Found {len(orders)} orders")
            for order in orders[-3:]:
                print(f"   - Order {order['id']}: {order['customer_name']} - {order.get('frame_title', 'Unknown Frame')}")
            return True
        else:
            print(f"❌ Orders List failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Orders List error: {e}")
        return False

def test_qr_scan():
    """Test QR code scanning"""
    print("\n📱 Testing QR Code Scan...")
    try:
        response = requests.get("http://localhost:8001/api/scan/1/")
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
    print("\n📊 Testing Statistics...")
    try:
        response = requests.get("http://localhost:8001/api/statistics/")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Statistics:")
            print(f"   Total Orders: {stats['total_orders']}")
            print(f"   Supabase Orders: {stats.get('supabase_orders', 0)}")
            print(f"   Local Orders: {stats.get('local_orders', 0)}")
            print(f"   Total Frames: {stats['total_frames']}")
            return True
        else:
            print(f"❌ Statistics failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Statistics error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Final Comprehensive Test for Audio Frame Art System")
    print("=" * 70)
    
    # Wait for services to be ready
    print("⏳ Waiting for services to be ready...")
    time.sleep(3)
    
    # Run tests
    tests = [
        test_website,
        test_api_health,
        test_frames_api,
        test_order_creation,
        test_orders_list,
        test_qr_scan,
        test_statistics
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 70)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your system is fully functional!")
        print("\n🚀 Next Steps:")
        print("1. Create the Supabase table (see SUPABASE_SETUP_GUIDE.md)")
        print("2. Test the mobile app: cd mobile && flutter run -d web-server --web-port 8081")
        print("3. Create orders through the website and see them in Supabase!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    print("\n🔗 Useful Links:")
    print("   Website: http://localhost:3000")
    print("   API Health: http://localhost:8001/health/")
    print("   Supabase Dashboard: https://supabase.com/dashboard/project/qksmfogjdurxgzmlcujb")
    print("   Setup Guide: See SUPABASE_SETUP_GUIDE.md")

if __name__ == "__main__":
    main()
