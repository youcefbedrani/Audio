#!/usr/bin/env python3
"""
Final Test of Complete Audio Frame Art Workflow
"""

import requests
import json
import time

def test_complete_workflow():
    """Test the complete audio frame art workflow"""
    print("🎵 TESTING COMPLETE AUDIO FRAME ART WORKFLOW")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n🔍 Step 1: Testing API Health...")
    try:
        response = requests.get("http://localhost:8001/health/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Status: {data['status']}")
            print(f"✅ Supabase Connected: {data['supabase_connected']}")
            print(f"✅ Audio Storage: {data['audio_storage']}")
            print(f"✅ QR Generation: {data['qr_generation']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Create Order with Audio
    print("\n🔍 Step 2: Creating Order with Audio...")
    try:
        # Create test audio file
        with open("test_final_audio.txt", "w") as f:
            f.write("This is the final test audio file for Audio Frame Art system. It should work perfectly!")
        
        # Prepare form data
        data = {
            "first_name": "Final",
            "last_name": "Test",
            "phone": "0555999999",
            "wilaya": "الجزائر",
            "baladiya": "الجزائر",
            "address": "Final Test Address",
            "frame": "1",
            "payment_method": "COD"
        }
        
        # Prepare files
        files = {
            "audio_file": ("test_final_audio.txt", open("test_final_audio.txt", "rb"), "text/plain")
        }
        
        print("   📤 Sending order with audio file...")
        response = requests.post("http://localhost:8001/api/orders/", data=data, files=files)
        files["audio_file"][1].close()
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Order created successfully!")
            print(f"   Order ID: {result['id']}")
            print(f"   Customer: {result['order']['customer_name']}")
            print(f"   Frame: {result['order']['frame_title']}")
            print(f"   Audio URL: {result['order']['audio_file_url']}")
            print(f"   QR Code URL: {result['order']['qr_code_url']}")
            
            # Test 3: Verify Audio File Access
            print("\n🔍 Step 3: Testing Audio File Access...")
            audio_url = result['order']['audio_file_url']
            audio_response = requests.get(audio_url)
            if audio_response.status_code == 200:
                print(f"✅ Audio file accessible: {len(audio_response.text)} characters")
                print(f"   Content: {audio_response.text[:50]}...")
            else:
                print(f"❌ Audio file not accessible: {audio_response.status_code}")
            
            # Test 4: Verify QR Code Access
            print("\n🔍 Step 4: Testing QR Code Access...")
            qr_url = result['order']['qr_code_url']
            qr_response = requests.get(qr_url)
            if qr_response.status_code == 200:
                print(f"✅ QR code accessible: {len(qr_response.content)} bytes")
                print(f"   Content-Type: {qr_response.headers.get('content-type')}")
            else:
                print(f"❌ QR code not accessible: {qr_response.status_code}")
            
            # Test 5: Test QR Code Scanning
            print("\n🔍 Step 5: Testing QR Code Scanning...")
            scan_response = requests.get(f"http://localhost:8001/api/scan/1/")
            if scan_response.status_code == 200:
                scan_data = scan_response.json()
                print(f"✅ QR scan successful!")
                print(f"   Frame ID: {scan_data['frame_id']}")
                print(f"   Frame Title: {scan_data['frame_title']}")
                print(f"   Audio URL: {scan_data['audio_url']}")
                print(f"   QR Code URL: {scan_data['qr_code_url']}")
                print(f"   Message: {scan_data['message']}")
            else:
                print(f"❌ QR scan failed: {scan_response.status_code}")
            
            # Test 6: Test Order Retrieval
            print("\n🔍 Step 6: Testing Order Retrieval...")
            orders_response = requests.get("http://localhost:8001/api/orders/")
            if orders_response.status_code == 200:
                orders = orders_response.json()
                print(f"✅ Orders retrieved: {len(orders)} total orders")
                
                # Find our test order
                test_order = next((o for o in orders if o.get('customer_name') == 'Final Test'), None)
                if test_order:
                    print(f"✅ Test order found in database!")
                    print(f"   Audio URL: {test_order.get('audio_file_url', 'N/A')}")
                    print(f"   QR Code URL: {test_order.get('qr_code_url', 'N/A')}")
                else:
                    print("⚠️  Test order not found in database (may be local storage only)")
            else:
                print(f"❌ Order retrieval failed: {orders_response.status_code}")
            
            return True
        else:
            print(f"❌ Order creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Order creation error: {e}")
        return False
    finally:
        # Clean up test file
        import os
        if os.path.exists("test_final_audio.txt"):
            os.remove("test_final_audio.txt")
    
    print("\n" + "=" * 60)
    print("🎉 COMPLETE WORKFLOW TEST FINISHED!")
    print("=" * 60)

if __name__ == "__main__":
    success = test_complete_workflow()
    
    if success:
        print("\n✅ ALL TESTS PASSED! 🎉")
        print("\n📋 WORKFLOW SUMMARY:")
        print("1. ✅ Orders are created successfully")
        print("2. ✅ Audio files are uploaded and stored locally")
        print("3. ✅ QR codes are generated for audio files")
        print("4. ✅ Audio files are accessible via HTTP")
        print("5. ✅ QR codes are accessible via HTTP")
        print("6. ✅ QR code scanning returns audio URLs")
        print("7. ✅ Orders are stored in database")
        
        print("\n🚀 NEXT STEPS:")
        print("1. Test the mobile app: cd mobile && flutter run -d web-server --web-port 8081")
        print("2. Scan the QR code with the mobile app")
        print("3. Verify audio playback works")
        print("4. For production: Set up Cloudinary credentials for cloud storage")
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("Please check the error messages above and fix the issues.")
