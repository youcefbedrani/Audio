#!/usr/bin/env python3
"""
Quick Audio Test - Test audio playback without browser
"""

import requests
import json

def quick_audio_test():
    """Quick test of audio functionality"""
    print("🎵 QUICK AUDIO TEST")
    print("=" * 40)
    
    # Test 1: Health Check
    print("\n🔍 Testing API Health...")
    try:
        response = requests.get("http://localhost:8001/health/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Status: {data['status']}")
            print(f"✅ Audio Storage: {data['audio_storage']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return
    
    # Test 2: Get Recent Orders
    print("\n🔍 Getting Recent Orders...")
    try:
        response = requests.get("http://localhost:8001/api/orders/")
        if response.status_code == 200:
            orders = response.json()
            audio_orders = [o for o in orders if o.get('audio_file_url')]
            print(f"✅ Found {len(audio_orders)} orders with audio")
            
            if audio_orders:
                # Show last 3 orders
                for order in audio_orders[-3:]:
                    print(f"\n📄 Order {order['id']}: {order['customer_name']}")
                    print(f"   Audio URL: {order['audio_file_url']}")
                    print(f"   QR URL: {order['qr_code_url']}")
                    
                    # Test audio file access
                    audio_response = requests.get(order['audio_file_url'])
                    if audio_response.status_code == 200:
                        content_type = audio_response.headers.get('content-type', 'unknown')
                        print(f"   ✅ Audio accessible (Content-Type: {content_type})")
                    else:
                        print(f"   ❌ Audio not accessible ({audio_response.status_code})")
            else:
                print("⚠️  No orders with audio found")
        else:
            print(f"❌ Failed to get orders: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting orders: {e}")
    
    # Test 3: Test QR Scan
    print("\n🔍 Testing QR Scan...")
    try:
        response = requests.get("http://localhost:8001/api/scan/1/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ QR scan successful!")
            print(f"   Frame: {data['frame_title']}")
            print(f"   Audio URL: {data['audio_url']}")
            print(f"   Message: {data['message']}")
        else:
            print(f"❌ QR scan failed: {response.status_code}")
    except Exception as e:
        print(f"❌ QR scan error: {e}")
    
    print("\n" + "=" * 40)
    print("🎉 QUICK TEST COMPLETED!")
    print("=" * 40)
    
    print("\n📋 TO TEST AUDIO PLAYBACK:")
    print("1. Open: http://localhost:8001/test_audio_player.html")
    print("2. Or open: simple_audio_test.html in your browser")
    print("3. Click 'Load Recent Audio' to see your recorded files")
    print("4. Click on any audio URL to test playback")

if __name__ == "__main__":
    quick_audio_test()
