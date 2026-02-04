#!/usr/bin/env python3

import requests
import json

# Supabase configuration
SUPABASE_URL = "https://qksmfogjdurxgzmlcujb.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrc21mb2dqZHVyeGd6bWxjdWpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA0NTg3OTEsImV4cCI6MjA3NjAzNDc5MX0.E1VDpkzcq3AzyPiNZOHU2_5IPyx2k76UdZZiaXg3CVk"

# Try with service role key (bypasses RLS)
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrc21mb2dqZHVyeGd6bWxjdWpiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDQ1ODc5MSwiZXhwIjoyMDc2MDM0NzkxfQ.YourServiceKeyHere"

headers = {
    "apikey": SUPABASE_ANON_KEY,
    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
    "Content-Type": "application/json"
}

# Test order data
order_data = {
    "customer_name": "Test User",
    "customer_phone": "0555123456",
    "customer_email": "test@example.com",
    "delivery_address": "Test Address",
    "city": "الجزائر الوسطى",
    "postal_code": "16000",
    "status": "pending",
    "payment_method": "COD",
    "frame_id": 1,
    "total_amount": 150.0,
    "notes": "Wilaya: الجزائر"
}

print("Testing order creation...")
print(f"Order data: {json.dumps(order_data, indent=2)}")

# Try to create order
response = requests.post(
    f"{SUPABASE_URL}/rest/v1/api_order",
    headers=headers,
    json=order_data
)

print(f"Response status: {response.status_code}")
print(f"Response text: {response.text}")

if response.status_code == 201:
    print("✅ Order created successfully!")
    order = response.json()
    print(f"Order ID: {order[0]['id'] if isinstance(order, list) else order['id']}")
else:
    print("❌ Failed to create order")
    print(f"Error: {response.text}")
