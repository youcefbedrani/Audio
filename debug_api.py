#!/usr/bin/env python3
"""
Debug script to test the API locally
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['DEBUG'] = True
CORS(app)

# Sample frame data
FRAMES_DATA = [
    {
        "id": 1,
        "title": "Test Frame",
        "description": "Test Description",
        "frame_type": "wooden",
        "price": 150.00,
        "is_available": True,
        "image": "https://example.com/image.jpg",
        "created_at": "2024-01-01T00:00:00Z"
    }
]

# In-memory storage
orders = []

@app.route('/api/orders/', methods=['POST'])
def handle_orders():
    """Handle order creation"""
    try:
        print("=== DEBUG START ===")
        print(f"Request method: {request.method}")
        print(f"Request content type: {request.content_type}")
        print(f"Request is JSON: {request.is_json}")
        
        # Check if request is JSON or form data
        if request.is_json:
            data = request.get_json()
            audio_file = None
            print("Processing JSON data")
        else:
            # Handle form data (including file uploads)
            data = request.form.to_dict()
            audio_file = request.files.get('audio_file')
            print("Processing form data")
        
        print(f"Data: {data}")
        print(f"Audio file: {audio_file}")
        
        # Validate required fields
        required_fields = ['customer_name', 'customer_phone', 'delivery_address', 'city']
        for field in required_fields:
            if field not in data:
                print(f"Missing field: {field}")
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Handle both 'frame' and 'frame_id' field names
        frame_id = data.get('frame') or data.get('frame_id')
        if not frame_id:
            print("Missing frame_id")
            return jsonify({"error": "Missing required field: frame or frame_id"}), 400
        
        print(f"Frame ID: {frame_id}")
        
        # Get frame price
        frame_id = int(frame_id)
        frame = next((f for f in FRAMES_DATA if f["id"] == frame_id), None)
        if not frame:
            print("Frame not found")
            return jsonify({"error": "Frame not found"}), 400
        
        print(f"Frame found: {frame}")
        
        # Create order
        order = {
            "id": len(orders) + 1,
            "customer_name": data["customer_name"],
            "customer_phone": data["customer_phone"],
            "delivery_address": data["delivery_address"],
            "city": data["city"],
            "frame_id": frame_id,
            "frame": frame,
            "status": "pending",
            "payment_method": "COD",
            "total_amount": float(frame["price"]),
            "created_at": datetime.now().isoformat(),
        }
        
        orders.append(order)
        print(f"Order created: {order}")
        print("=== DEBUG END ===")
        
        return jsonify({
            "id": order["id"],
            "message": "Order created successfully",
            "order": order
        }), 201
        
    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Debug API...")
    app.run(host='0.0.0.0', port=8002, debug=True)
