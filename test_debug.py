#!/usr/bin/env python3
"""
Test script for debug API
"""

import requests
import json

# Test the debug API
url = "http://localhost:8002/api/orders/"

# Test data
data = {
    "customer_name": "Test User",
    "customer_phone": "0555123456", 
    "delivery_address": "Test Address",
    "city": "Algiers",
    "frame": "1",
    "payment_method": "COD"
}

print("Testing debug API with form data...")
try:
    response = requests.post(url, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
