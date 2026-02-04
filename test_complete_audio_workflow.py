#!/usr/bin/env python3
"""
Test Complete Audio Workflow: Order Creation, Audio Upload, QR Generation, and Mobile Scanning
"""

import requests
import json
import time
import os

def test_health():
    """Test API health"""
    print("🔍 Testing API Health...")
    try:
        response = requests.get("http://localhost:8001/health/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Health: {data['status']}")
            print(f"   Supabase Connected: {data['supabase_connected']}")
            print(f"   Cloudinary Configured: {data.get('cloudinary_configured', False)}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_frames():
    """Test frames API"""
    print("\n🔍 Testing Frames API...")
    try:
        response = requests.get("http://localhost:8001/api/frames/")
        if response.status_code == 200:
            frames = response.json()
            print(f"✅ Frames API: Found {len(frames)} frames")
            for frame in frames[:2]:  # Show first 2 frames
                print(f"   - {frame['id']}: {frame['title']} ({frame['price']} دج)")
            return True
        else:
            print(f"❌ Frames API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frames API error: {e}")
        return False

def create_test_audio_file():
    """Create a test audio file"""
    print("\n🔍 Creating test audio file...")
    try:
        # Create a simple test audio file (just a text file for testing)
        test_content = "This is a test audio file for Audio Frame Art system."
        with open("test_audio.txt", "w") as f:
            f.write(test_content)
        print("✅ Test audio file created: test_audio.txt")
        return "test_audio.txt"
    except Exception as e:
        print(f"❌ Error creating test audio file: {e}")
        return None

def test_order_creation_with_audio():
    """Test order creation with audio upload"""
    print("\n🔍 Testing Order Creation with Audio Upload...")
    
    # Create test audio file
    audio_file = create_test_audio_file()
    if not audio_file:
        return False
    
    try:
        # Prepare form data
        data = {
            "first_name": "Test",
            "last_name": "User Audio",
            "phone": "0555123456",
            "wilaya": "الجزائر",
            "baladiya": "الجزائر",
            "address": "Test Address with Audio",
            "frame": "1",
            "payment_method": "COD"
        }
        
        # Prepare files
        files = {
            "audio_file": ("test_audio.txt", open(audio_file, "rb"), "text/plain")
        }
        
        print("   Sending order with audio file...")
        response = requests.post("http://localhost:8001/api/orders/", data=data, files=files)
        
        # Close file
        files["audio_file"][1].close()
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Order created successfully!")
            print(f"   Order ID: {result['id']}")
            print(f"   Message: {result['message']}")
            
            if result.get("audio_uploaded"):
                print(f"   Audio URL: {result.get('audio_url', 'N/A')}")
            if result.get("qr_generated"):
                print(f"   QR Code URL: {result.get('qr_url', 'N/A')}")
            
            return result["id"]
        else:
            print(f"❌ Order creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Order creation error: {e}")
        return None
    finally:
        # Clean up test file
        if os.path.exists(audio_file):
            os.remove(audio_file)

def test_qr_scanning(order_id):
    """Test QR code scanning"""
    print(f"\n🔍 Testing QR Code Scanning for Order {order_id}...")
    try:
        response = requests.get(f"http://localhost:8001/api/scan/1/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ QR Scan successful!")
            print(f"   Frame ID: {data['frame_id']}")
            print(f"   Frame Title: {data['frame_title']}")
            print(f"   Audio URL: {data.get('audio_url', 'N/A')}")
            print(f"   QR Code URL: {data.get('qr_code_url', 'N/A')}")
            print(f"   Message: {data['message']}")
            return True
        else:
            print(f"❌ QR scan failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ QR scan error: {e}")
        return False

def test_orders_list():
    """Test orders list from Supabase"""
    print("\n🔍 Testing Orders List from Supabase...")
    try:
        response = requests.get("http://localhost:8001/api/orders/")
        if response.status_code == 200:
            orders = response.json()
            print(f"✅ Orders list: Found {len(orders)} orders")
            for order in orders[-2:]:  # Show last 2 orders
                print(f"   - Order {order['id']}: {order['customer_name']} ({order['city']})")
                if order.get('audio_file_url'):
                    print(f"     Audio: {order['audio_file_url'][:50]}...")
                if order.get('qr_code_url'):
                    print(f"     QR Code: {order['qr_code_url'][:50]}...")
            return True
        else:
            print(f"❌ Orders list failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Orders list error: {e}")
        return False

def test_statistics():
    """Test statistics API"""
    print("\n🔍 Testing Statistics API...")
    try:
        response = requests.get("http://localhost:8001/api/statistics/")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Statistics retrieved:")
            print(f"   Total Orders: {stats['total_orders']}")
            print(f"   Total Frames: {stats['total_frames']}")
            print(f"   Orders with Audio: {stats.get('orders_with_audio', 0)}")
            return True
        else:
            print(f"❌ Statistics failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Statistics error: {e}")
        return False

def main():
    """Run complete test suite"""
    print("🧪 COMPLETE AUDIO WORKFLOW TEST")
    print("=" * 50)
    
    # Test 1: Health Check
    if not test_health():
        print("\n❌ Health check failed. Make sure the API is running.")
        return
    
    # Test 2: Frames API
    if not test_frames():
        print("\n❌ Frames API failed.")
        return
    
    # Test 3: Order Creation with Audio
    order_id = test_order_creation_with_audio()
    if not order_id:
        print("\n❌ Order creation with audio failed.")
        return
    
    # Wait a moment for processing
    print("\n⏳ Waiting for processing...")
    time.sleep(2)
    
    # Test 4: QR Code Scanning
    test_qr_scanning(order_id)
    
    # Test 5: Orders List
    test_orders_list()
    
    # Test 6: Statistics
    test_statistics()
    
    print("\n" + "=" * 50)
    print("🎉 COMPLETE AUDIO WORKFLOW TEST COMPLETED!")
    print("=" * 50)
    print("\n📱 To test mobile app:")
    print("   cd mobile && flutter run -d web-server --web-port 8081")
    print("\n🌐 To test website:")
    print("   http://localhost:3000")
    print("\n🔗 To test API directly:")
    print("   http://localhost:8001/health/")

if __name__ == "__main__":
    main()
