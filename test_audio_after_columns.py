#!/usr/bin/env python3
"""
Test Audio Workflow After Adding Supabase Columns
"""

import requests
import json
import time

def test_audio_workflow():
    """Test complete audio workflow after adding Supabase columns"""
    print("🧪 TESTING AUDIO WORKFLOW AFTER ADDING SUPABASE COLUMNS")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n🔍 Testing API Health...")
    try:
        response = requests.get("http://localhost:8001/health/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Health: {data['status']}")
            print(f"   Supabase Connected: {data['supabase_connected']}")
            print(f"   Cloudinary Configured: {data.get('cloudinary_configured', False)}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return
    
    # Test 2: Create Order with Audio
    print("\n🔍 Testing Order Creation with Audio...")
    try:
        # Create test audio file
        with open("test_audio.txt", "w") as f:
            f.write("This is a test audio file for Audio Frame Art system.")
        
        # Prepare form data
        data = {
            "first_name": "Test",
            "last_name": "Audio User",
            "phone": "0555123456",
            "wilaya": "الجزائر",
            "baladiya": "الجزائر",
            "address": "Test Address with Audio",
            "frame": "1",
            "payment_method": "COD"
        }
        
        # Prepare files
        files = {
            "audio_file": ("test_audio.txt", open("test_audio.txt", "rb"), "text/plain")
        }
        
        print("   Sending order with audio file...")
        response = requests.post("http://localhost:8001/api/orders/", data=data, files=files)
        files["audio_file"][1].close()
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Order created successfully!")
            print(f"   Order ID: {result['id']}")
            print(f"   Message: {result['message']}")
            
            if "supabase_id" in result:
                print(f"   Supabase ID: {result['supabase_id']}")
                print("✅ Order saved to Supabase!")
            else:
                print("⚠️  Order saved locally (Supabase columns may not be added yet)")
            
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
        import os
        if os.path.exists("test_audio.txt"):
            os.remove("test_audio.txt")
    
    # Test 3: Check Supabase Orders
    print("\n🔍 Checking Supabase Orders...")
    try:
        response = requests.get("http://localhost:8001/api/orders/")
        if response.status_code == 200:
            orders = response.json()
            print(f"✅ Found {len(orders)} orders in Supabase")
            
            # Look for orders with audio
            audio_orders = [o for o in orders if o.get('audio_file_url')]
            if audio_orders:
                print(f"✅ Found {len(audio_orders)} orders with audio files!")
                for order in audio_orders[-2:]:  # Show last 2
                    print(f"   - Order {order['id']}: {order['customer_name']}")
                    print(f"     Audio: {order.get('audio_file_url', 'N/A')[:50]}...")
                    print(f"     QR Code: {order.get('qr_code_url', 'N/A')[:50]}...")
            else:
                print("⚠️  No orders with audio files found")
                print("   Make sure you added the audio columns to Supabase!")
        else:
            print(f"❌ Failed to fetch orders: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking orders: {e}")
    
    # Test 4: QR Code Scanning
    print("\n🔍 Testing QR Code Scanning...")
    try:
        response = requests.get("http://localhost:8001/api/scan/1/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ QR Scan successful!")
            print(f"   Frame ID: {data['frame_id']}")
            print(f"   Audio URL: {data.get('audio_url', 'N/A')}")
            print(f"   QR Code URL: {data.get('qr_code_url', 'N/A')}")
            print(f"   Message: {data['message']}")
        else:
            print(f"❌ QR scan failed: {response.status_code}")
    except Exception as e:
        print(f"❌ QR scan error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 AUDIO WORKFLOW TEST COMPLETED!")
    print("=" * 60)
    
    print("\n📋 NEXT STEPS:")
    print("1. Add audio columns to Supabase table:")
    print("   - audio_file_url (text)")
    print("   - qr_code_url (text)")
    print("   - qr_code_data (text)")
    print("2. Run this test again to verify audio uploads work")
    print("3. Test mobile app: cd mobile && flutter run -d web-server --web-port 8081")

if __name__ == "__main__":
    test_audio_workflow()
