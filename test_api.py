#!/usr/bin/env python3
"""
Test script to debug the API issue
"""

import requests
import json

# Test the API
url = "http://localhost:8001/api/orders/"

# Test data
data = {
    "customer_name": "Test User",
    "customer_phone": "0555123456", 
    "delivery_address": "Test Address",
    "city": "Algiers",
    "wilaya": "الجزائر",
    "baladya": "الجزائر",
    "frame": "1",
    "payment_method": "COD"
}

print("Testing API with form data...")
try:
    response = requests.post(url, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

print("\nTesting API with JSON data...")
try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
