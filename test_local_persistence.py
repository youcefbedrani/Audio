import requests
import json

import os
PORT = os.getenv('PORT', '8180')
BASE_URL = f"http://localhost:{PORT}"

def test_order_and_scan():
    print("🚀 Testing order creation with local fallback...")
    
    # 1. Create Order
    order_data = {
        "customer_name": "Test User",
        "phone": "0555555555",
        "address": "Test Street",
        "city": "Algiers",
        "frame": 1
    }
    
    response = requests.post(f"{BASE_URL}/api/orders/", data=order_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code != 201:
        print("❌ Failed to create order")
        return
    
    scan_id = response.json().get("scan_id")
    print(f"✅ Created order with Scan ID: {scan_id}")
    
    # 2. Test Scan Lookup
    print(f"\n🔍 Testing scan lookup for ID: {scan_id}...")
    scan_response = requests.get(f"{BASE_URL}/api/audio/{scan_id}/")
    print(f"Status: {scan_response.status_code}")
    print(f"Response: {json.dumps(scan_response.json(), indent=2)}")
    
    if scan_response.status_code == 200 and scan_response.json().get("success"):
        print("✅ Scan lookup successful!")
    else:
        print("❌ Scan lookup failed")

if __name__ == "__main__":
    test_order_and_scan()
