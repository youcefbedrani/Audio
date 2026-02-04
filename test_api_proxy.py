#!/usr/bin/env python3

import requests
import json

# Test the API proxy
print("Testing API proxy...")

# Test frames endpoint
try:
    response = requests.get('http://localhost:8001/api/frames/')
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Frames API working: {len(data.get('results', []))} frames")
    else:
        print(f"❌ Frames API error: {response.status_code}")
except Exception as e:
    print(f"❌ Frames API error: {e}")

# Test order endpoint
try:
    order_data = {
        'first_name': 'Test',
        'last_name': 'User',
        'phone': '0555123456',
        'wilaya': 'الجزائر',
        'baladiya': 'الجزائر الوسطى',
        'address': 'Test Address',
        'payment_method': 'COD',
        'frame': '1'
    }
    
    response = requests.post('http://localhost:8001/api/orders/', data=order_data)
    print(f"Order API response: {response.status_code}")
    print(f"Order API response: {response.text}")
    
    if response.status_code == 200:
        print("✅ Order API working")
    else:
        print(f"❌ Order API error: {response.status_code}")
        
except Exception as e:
    print(f"❌ Order API error: {e}")

