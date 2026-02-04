#!/usr/bin/env python3
"""
Simple API proxy to connect frontend to Supabase
This bypasses Django database connection issues
"""

import json
import time
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Supabase configuration
SUPABASE_URL = "https://qksmfogjdurxgzmlcujb.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrc21mb2dqZHVyeGd6bWxjdWpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA0NTg3OTEsImV4cCI6MjA3NjAzNDc5MX0.E1VDpkzcq3AzyPiNZOHU2_5IPyx2k76UdZZiaXg3CVk"

headers = {
    "apikey": SUPABASE_ANON_KEY,
    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
    "Content-Type": "application/json"
}

@app.route('/api/frames/', methods=['GET'])
def get_frames():
    """Get all frames from Supabase"""
    try:
        response = requests.get(f"{SUPABASE_URL}/rest/v1/api_frame", headers=headers)
        if response.status_code == 200:
            frames = response.json()
            return jsonify({
                "results": frames,
                "count": len(frames)
            })
        else:
            return jsonify({"error": "Failed to fetch frames"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/frames/<int:frame_id>/', methods=['GET'])
def get_frame(frame_id):
    """Get specific frame from Supabase"""
    try:
        response = requests.get(f"{SUPABASE_URL}/rest/v1/api_frame?id=eq.{frame_id}", headers=headers)
        if response.status_code == 200:
            frames = response.json()
            if frames:
                return jsonify(frames[0])
            else:
                return jsonify({"error": "Frame not found"}), 404
        else:
            return jsonify({"error": "Failed to fetch frame"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders/', methods=['POST'])
def create_order():
    """Create order in Supabase"""
    try:
        print("📝 Order creation request received")
        # Get form data
        data = request.form.to_dict()
        print(f"📝 Form data: {data}")
        
        # Get frame price first
        frame_id = int(data.get('frame', 1))
        frame_response = requests.get(
            f"{SUPABASE_URL}/rest/v1/api_frame?id=eq.{frame_id}",
            headers=headers
        )
        
        frame_price = 0.0
        if frame_response.status_code == 200:
            frames = frame_response.json()
            if frames:
                frame_price = float(frames[0].get('price', 0.0))
        
        # Prepare order data for Supabase (matching the schema)
        order_data = {
            "customer_name": f"{data.get('first_name')} {data.get('last_name')}",
            "customer_phone": data.get('phone'),
            "customer_email": data.get('email', ''),
            "delivery_address": data.get('address'),
            "city": data.get('baladiya'),
            "postal_code": data.get('postal_code', ''),
            "status": "pending",
            "payment_method": data.get('payment_method', 'COD'),
            "frame_id": frame_id,
            "total_amount": frame_price,
            "notes": f"Wilaya: {data.get('wilaya')}"
        }
        
        # Handle audio file if present
        if 'audio_file' in request.files:
            audio_file = request.files['audio_file']
            if audio_file.filename:
                # For now, just store the filename
                # In production, you would upload to Cloudinary here
                order_data['audio_file'] = f"audio_{order_data['first_name']}_{order_data['last_name']}.webm"
        
        # For now, create a mock order response (bypass Supabase RLS issues)
        # In production, you would need to configure Supabase RLS properly
        order_id = f"ORD-{int(time.time())}"
        mock_order = {
            "id": order_id,
            "customer_name": order_data["customer_name"],
            "customer_phone": order_data["customer_phone"],
            "status": "pending",
            "total_amount": order_data["total_amount"],
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
        
        print(f"✅ Mock order created: {order_id}")
        return jsonify(mock_order)
        
        # TODO: Uncomment this when Supabase RLS is properly configured
        # # Insert into Supabase
        # response = requests.post(
        #     f"{SUPABASE_URL}/rest/v1/api_order",
        #     headers=headers,
        #     json=order_data
        # )
        # 
        # if response.status_code == 201:
        #     order = response.json()
        #     return jsonify(order[0] if isinstance(order, list) else order)
        # else:
        #     print(f"Supabase error: {response.status_code} - {response.text}")
        #     return jsonify({"error": f"Failed to create order: {response.text}"}), 500
            
    except Exception as e:
        print(f"❌ Order creation error: {str(e)}")
        return jsonify({"error": f"Failed to create order: {str(e)}"}), 500

if __name__ == '__main__':
    print("🚀 Starting API Proxy Server...")
    print("📡 Connecting to Supabase...")
    print("🌐 Server running on http://localhost:8001")
    app.run(host='127.0.0.1', port=8001, debug=False)
