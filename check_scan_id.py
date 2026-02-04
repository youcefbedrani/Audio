import requests
import json
import os

SUPABASE_URL = "https://qksmfogjdurxgzmlcujb.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrc21mb2dqZHVyeGd6bWxjdWpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA0NTg3OTEsImV4cCI6MjA3NjAzNDc5MX0.E1VDpkzcq3AzyPiNZOHU2_5IPyx2k76UdZZiaXg3CVk"
SCAN_ID = "15EFF456AE9C404"

def check_scan_id():
    url = f"{SUPABASE_URL}/rest/v1/api_order?scan_id=eq.{SCAN_ID}&select=*"
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:
            print(f"✅ Found order: {json.dumps(data[0], indent=2)}")
        else:
            print(f"❌ No order found with scan_id: {SCAN_ID}")
            
            # Check for partial matches or other similar IDs
            print("Checking all orders...")
            url_all = f"{SUPABASE_URL}/rest/v1/api_order?select=id,scan_id,customer_name&limit=5"
            response_all = requests.get(url_all, headers=headers)
            if response_all.status_code == 200:
                print(f"Sample orders: {json.dumps(response_all.json(), indent=2)}")
    else:
        print(f"❌ Error querying Supabase: {response.status_code} - {response.text}")

if __name__ == "__main__":
    check_scan_id()
