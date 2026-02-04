#!/usr/bin/env python3
"""
Complete flow test for Audio Frame Art system
Tests the entire user journey from order creation to QR scanning
"""

import requests
import json
import time

# Test configuration
API_BASE_URL = "http://localhost:8001"
FRONTEND_URL = "http://localhost:3000"

def test_api_health():
    """Test API health"""
    print("🔍 Testing API health...")
    try:
        response = requests.get(f"{API_BASE_URL}/health/")
        if response.status_code == 200:
            print("✅ API is healthy")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API health check error: {e}")
        return False

def test_frames_api():
    """Test frames API"""
    print("\n🔍 Testing frames API...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/frames/")
        if response.status_code == 200:
            frames = response.json()
            print(f"✅ Frames API working - {len(frames)} frames available")
            return frames
        else:
            print(f"❌ Frames API failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Frames API error: {e}")
        return None

def test_order_creation():
    """Test order creation"""
    print("\n🔍 Testing order creation...")
    try:
        # Test with form data (like frontend would send)
        order_data = {
            "customer_name": "Test User",
            "customer_phone": "0555123456",
            "delivery_address": "123 Test Street, Algiers",
            "city": "Algiers",
            "wilaya": "الجزائر",
            "baladya": "الجزائر",
            "frame": "1",
            "payment_method": "COD"
        }
        
        response = requests.post(f"{API_BASE_URL}/api/orders/", data=order_data)
        if response.status_code == 201:
            order = response.json()
            print(f"✅ Order created successfully - ID: {order['id']}")
            return order
        else:
            print(f"❌ Order creation failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Order creation error: {e}")
        return None

def test_qr_scanning(frame_id):
    """Test QR code scanning"""
    print(f"\n🔍 Testing QR code scanning for frame {frame_id}...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/scan/{frame_id}/")
        if response.status_code == 200:
            scan_data = response.json()
            print(f"✅ QR scan successful - Frame: {scan_data['frame_title']}")
            print(f"   Audio URL: {scan_data['audio_url']}")
            return scan_data
        else:
            print(f"❌ QR scan failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ QR scan error: {e}")
        return None

def test_audio_play_tracking(frame_id):
    """Test audio play tracking"""
    print(f"\n🔍 Testing audio play tracking for frame {frame_id}...")
    try:
        response = requests.post(f"{API_BASE_URL}/api/track-play/{frame_id}/")
        if response.status_code == 200:
            track_data = response.json()
            print(f"✅ Audio play tracked - Plays: {track_data['plays_count']}")
            return track_data
        else:
            print(f"❌ Audio play tracking failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Audio play tracking error: {e}")
        return None

def test_statistics():
    """Test statistics API"""
    print("\n🔍 Testing statistics API...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/statistics/")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Statistics retrieved:")
            print(f"   Total orders: {stats['total_orders']}")
            print(f"   Total frames: {stats['total_frames']}")
            print(f"   Total scans: {stats['total_scans']}")
            print(f"   Total plays: {stats['total_plays']}")
            return stats
        else:
            print(f"❌ Statistics API failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Statistics API error: {e}")
        return None

def test_frontend_access():
    """Test frontend access"""
    print("\n🔍 Testing frontend access...")
    try:
        response = requests.get(FRONTEND_URL)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            return True
        else:
            print(f"❌ Frontend access failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend access error: {e}")
        return False

def main():
    """Run complete flow test"""
    print("🚀 Starting Audio Frame Art Complete Flow Test")
    print("=" * 50)
    
    # Test 1: API Health
    if not test_api_health():
        print("\n❌ API health check failed. Stopping tests.")
        return
    
    # Test 2: Frames API
    frames = test_frames_api()
    if not frames:
        print("\n❌ Frames API failed. Stopping tests.")
        return
    
    # Test 3: Order Creation
    order = test_order_creation()
    if not order:
        print("\n❌ Order creation failed. Stopping tests.")
        return
    
    # Test 4: QR Scanning
    frame_id = 1  # Use first frame
    scan_data = test_qr_scanning(frame_id)
    if not scan_data:
        print("\n❌ QR scanning failed. Stopping tests.")
        return
    
    # Test 5: Audio Play Tracking
    track_data = test_audio_play_tracking(frame_id)
    if not track_data:
        print("\n❌ Audio play tracking failed. Stopping tests.")
        return
    
    # Test 6: Statistics
    stats = test_statistics()
    if not stats:
        print("\n❌ Statistics API failed. Stopping tests.")
        return
    
    # Test 7: Frontend Access
    frontend_ok = test_frontend_access()
    
    # Summary
    print("\n" + "=" * 50)
    print("🎉 COMPLETE FLOW TEST SUMMARY")
    print("=" * 50)
    
    if order and scan_data and track_data and stats and frontend_ok:
        print("✅ ALL TESTS PASSED!")
        print("\n🎯 System is working correctly:")
        print(f"   - Orders can be created (Order ID: {order['id']})")
        print(f"   - QR codes can be scanned (Frame: {scan_data['frame_title']})")
        print(f"   - Audio plays can be tracked (Plays: {track_data['plays_count']})")
        print(f"   - Statistics are available (Total orders: {stats['total_orders']})")
        print(f"   - Frontend is accessible")
        print("\n🚀 The system is ready for production!")
    else:
        print("❌ Some tests failed. Check the output above for details.")
    
    print("\n📱 Next steps:")
    print("   1. Test the mobile app QR scanning")
    print("   2. Test audio file uploads")
    print("   3. Test the complete user journey in the browser")

if __name__ == "__main__":
    main()
