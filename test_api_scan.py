import requests
import time
import sys

BASE_URL = "http://localhost:8001/api"

def test_scanning_flow():
    print("🚀 Testing Waveform ID Scanning Flow")
    
    # 1. Create a frame order (we don't need real audio for this metadata test)
    # We will mock the order creation
    print("\n1. creating test order...")
    try:
        # We need to simulate form data
        data = {
            "customer_name": "Test User",
            "customer_phone": "1234567890",
            "delivery_address": "Test Address",
            "city": "Test City",
            "frame_id": "1",
            "notes": "Test Order"
        }
        
        # We also need a dummy audio file
        # Use real audio file if available, to pass librosa check
        try:
             with open('test_audio.mp3', 'rb') as f:
                 audio_content = f.read()
        except FileNotFoundError:
             print("⚠️ test_audio.mp3 not found, using dummy content (might fail analysis)")
             audio_content = b'dummy'

        files = {
            'audio_file': ('test.mp3', audio_content, 'audio/mpeg')
        }
        
        response = requests.post(f"{BASE_URL}/orders/", data=data, files=files)
        
        if response.status_code != 201:
            print(f"❌ Failed to create order: {response.text}")
            return False
            
        result = response.json()
        print(f"✅ Order created: ID={result['id']}")
        
        # Get the scan_id
        order_data = result.get('order', {})
        scan_id = order_data.get('scan_id')
        
        if not scan_id:
            print("❌ No scan_id found in order response!")
            print(f"Response: {result}")
            return False
            
        print(f"✅ Received Scan ID: {scan_id}")
        
        # 2. Test Scanning with Alphabetic ID
        print(f"\n2. Testing scan with ID: {scan_id}")
        scan_response = requests.get(f"{BASE_URL}/scan/{scan_id}/")
        
        if scan_response.status_code != 200:
            print(f"❌ Scan failed: {scan_response.text}")
            return False
            
        scan_result = scan_response.json()
        print(f"✅ Scan processed: {scan_result.get('message')}")
        
        # Verify audio URL matches
        if scan_result.get('audio_url') == order_data.get('audio_file_url'):
            print("✅ Audio URL matches!")
        else:
            print(f"❌ Audio URL mismatch: {scan_result.get('audio_url')} vs {order_data.get('audio_file_url')}")
            return False
            
        # 3. Test Falback Logic (e.g. random ID should fail)
        print("\n3. Testing invalid ID...")
        bad_response = requests.get(f"{BASE_URL}/scan/INVALID-ID-123/")
        bad_result = bad_response.json()
        
        if not bad_result.get('audio_url'):
             print("✅ Invalid ID correctly returned no audio")
        else:
             print("❌ Invalid ID returned audio? " +  str(bad_result))
             return False

        return True
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    time.sleep(2) # Wait for server if just started
    if test_scanning_flow():
        print("\n✅ TEST PASSED: Waveform ID scanning is working!")
        sys.exit(0)
    else:
        print("\n❌ TEST FAILED")
        sys.exit(1)
