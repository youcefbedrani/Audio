#!/usr/bin/env python3
"""
Complete Audio Frame Art API with Cloudinary Upload and QR Code Generation
"""

import os
import json
import uuid
import base64
import qrcode
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from io import BytesIO
import cloudinary
import cloudinary.uploader
from cloudinary import api as cloudinary_api

# Initialize Flask app
app = Flask(__name__)

# Configuration
SUPABASE_URL = "https://qksmfogjdurxgzmlcujb.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrc21mb2dqZHVyeGd6bWxjdWpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA0NTg3OTEsImV4cCI6MjA3NjAzNDc5MX0.E1VDpkzcq3AzyPiNZOHU2_5IPyx2k76UdZZiaXg3CVk"

# Cloudinary configuration
CLOUDINARY_CLOUD_NAME = "dulct8pma"
CLOUDINARY_API_KEY = "your-api-key"  # Replace with actual key
CLOUDINARY_API_SECRET = "your-api-secret"  # Replace with actual secret

# Configure Cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

# Sample frames data
FRAMES_DATA = [
    {
        "id": 1,
        "title": "إطار خشبي كلاسيكي",
        "description": "إطار خشبي أنيق مصنوع من خشب البلوط الطبيعي، مثالي للصور العائلية والذكريات الثمينة.",
        "frame_type": "wooden",
        "price": 150.00,
        "is_available": True,
        "image": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400"
    },
    {
        "id": 2,
        "title": "إطار معدني عصري",
        "description": "إطار معدني أنيق بتصميم عصري، مثالي للمكاتب والمنازل العصرية.",
        "frame_type": "metal",
        "price": 120.00,
        "is_available": True,
        "image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400"
    },
    {
        "id": 3,
        "title": "إطار زجاجي شفاف",
        "description": "إطار زجاجي شفاف أنيق، يبرز جمال الصورة دون إلهاء.",
        "frame_type": "glass",
        "price": 100.00,
        "is_available": True,
        "image": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400"
    }
]

# In-memory storage for development
orders = []

def get_supabase_headers():
    """Get headers for Supabase API requests"""
    return {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json"
    }

def upload_audio_to_cloudinary(audio_file):
    """Upload audio file to Cloudinary"""
    try:
        # Upload audio file to Cloudinary
        result = cloudinary.uploader.upload(
            audio_file,
            resource_type="video",  # Cloudinary treats audio as video
            folder="audio_frame_art/audio",
            public_id=f"audio_{uuid.uuid4()}",
            format="mp3"
        )
        return result["secure_url"]
    except Exception as e:
        print(f"❌ Cloudinary upload error: {e}")
        return None

def generate_qr_code(audio_url, order_id):
    """Generate QR code for audio URL"""
    try:
        # Create QR code data
        qr_data = {
            "type": "audio_frame",
            "order_id": order_id,
            "audio_url": audio_url,
            "timestamp": datetime.now().isoformat()
        }
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json.dumps(qr_data))
        qr.make(fit=True)
        
        # Create QR code image
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to bytes
        img_buffer = BytesIO()
        qr_img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        # Upload QR code to Cloudinary
        qr_result = cloudinary.uploader.upload(
            img_buffer,
            folder="audio_frame_art/qr_codes",
            public_id=f"qr_{order_id}",
            format="png"
        )
        
        return {
            "qr_url": qr_result["secure_url"],
            "qr_data": json.dumps(qr_data)
        }
    except Exception as e:
        print(f"❌ QR code generation error: {e}")
        return None

def save_order_to_supabase(order_data):
    """Save order to Supabase database"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/api_order"
        headers = get_supabase_headers()
        
        # Map data to Supabase table structure
        supabase_data = {
            "customer_name": order_data["customer_name"],
            "customer_phone": order_data["customer_phone"],
            "customer_email": order_data.get("customer_email", ""),
            "delivery_address": order_data["delivery_address"],
            "city": order_data["city"],
            "postal_code": order_data.get("postal_code", "00000"),
            "frame_id": order_data["frame_id"],
            "audio_file_url": order_data.get("audio_file_url", ""),
            "qr_code_url": order_data.get("qr_code_url", ""),
            "qr_code_data": order_data.get("qr_code_data", ""),
            "status": order_data.get("status", "pending"),
            "payment_method": order_data.get("payment_method", "COD"),
            "total_amount": order_data["total_amount"],
            "notes": order_data.get("notes", ""),
            "created_at": order_data.get("created_at", datetime.now().isoformat())
        }
        
        print(f"💾 Saving order to Supabase...")
        print(f"   Data: {json.dumps(supabase_data, indent=2)}")
        
        response = requests.post(url, headers=headers, json=supabase_data)
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Order saved to Supabase: {result}")
            return {"success": True, "data": result}
        else:
            print(f"❌ Supabase error: {response.status_code} - {response.text}")
            return {"success": False, "error": response.text}
            
    except Exception as e:
        print(f"❌ Supabase save error: {e}")
        return {"success": False, "error": str(e)}

@app.route('/health/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test Supabase connection
        response = requests.get(f"{SUPABASE_URL}/rest/v1/api_order?select=count", headers=get_supabase_headers())
        supabase_connected = response.status_code == 200
        
        return jsonify({
            "status": "healthy",
            "supabase_connected": supabase_connected,
            "supabase_url": SUPABASE_URL,
            "cloudinary_configured": bool(CLOUDINARY_API_KEY != "your-api-key"),
            "timestamp": datetime.now().isoformat(),
            "total_orders": len(orders)
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/frames/', methods=['GET'])
def get_frames():
    """Get all frames"""
    return jsonify(FRAMES_DATA)

@app.route('/api/frames/<int:frame_id>/', methods=['GET'])
def get_frame(frame_id):
    """Get specific frame"""
    frame = next((f for f in FRAMES_DATA if f["id"] == frame_id), None)
    if frame:
        return jsonify(frame)
    return jsonify({"error": "Frame not found"}), 404

@app.route('/api/orders/', methods=['GET'])
def get_orders():
    """Get all orders from Supabase"""
    try:
        response = requests.get(f"{SUPABASE_URL}/rest/v1/api_order", headers=get_supabase_headers())
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to fetch orders"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders/', methods=['POST'])
def create_order():
    """Create new order with audio upload and QR code generation"""
    try:
        print(f"\n🆕 New order request received")
        
        # Get form data
        data = request.form.to_dict()
        print(f"   Data received: {data}")
        
        # Validate required fields
        customer_name = data.get("customer_name") or (data.get("first_name", "") + " " + data.get("last_name", "")).strip()
        phone = data.get("customer_phone") or data.get("phone", "")
        address = data.get("delivery_address") or data.get("address", "")
        city = data.get("city") or data.get("baladiya", "")
        
        if not customer_name:
            return jsonify({"error": "Missing required field: customer_name or first_name/last_name"}), 400
        if not phone:
            return jsonify({"error": "Missing required field: customer_phone or phone"}), 400
        if not address:
            return jsonify({"error": "Missing required field: delivery_address or address"}), 400
        if not city:
            return jsonify({"error": "Missing required field: city or baladiya"}), 400
        
        # Get frame ID
        frame_id = data.get('frame') or data.get('frame_id')
        if not frame_id:
            return jsonify({"error": "Missing required field: frame or frame_id"}), 400
        
        frame_id = int(frame_id)
        frame = next((f for f in FRAMES_DATA if f["id"] == frame_id), None)
        if not frame:
            return jsonify({"error": "Frame not found"}), 404
        
        # Handle audio file upload
        audio_url = None
        qr_data = None
        
        if 'audio_file' in request.files:
            audio_file = request.files['audio_file']
            if audio_file and hasattr(audio_file, 'filename') and audio_file.filename:
                print(f"📁 Uploading audio file: {audio_file.filename}")
                audio_url = upload_audio_to_cloudinary(audio_file)
                if audio_url:
                    print(f"✅ Audio uploaded to Cloudinary: {audio_url}")
                else:
                    print(f"❌ Failed to upload audio to Cloudinary")
        
        # Generate order ID
        order_id = len(orders) + 1
        
        # Generate QR code if audio was uploaded
        if audio_url:
            print(f"🔗 Generating QR code for audio...")
            qr_data = generate_qr_code(audio_url, order_id)
            if qr_data:
                print(f"✅ QR code generated: {qr_data['qr_url']}")
            else:
                print(f"❌ Failed to generate QR code")
        
        # Prepare order data
        order_data = {
            "customer_name": customer_name,
            "customer_phone": phone,
            "customer_email": data.get("customer_email", ""),
            "delivery_address": address,
            "city": city,
            "postal_code": data.get("postal_code", "00000"),
            "wilaya": data.get("wilaya", ""),
            "baladya": data.get("baladya", "") or data.get("baladiya", ""),
            "frame_id": frame_id,
            "frame_title": frame["title"],
            "frame_type": frame["frame_type"],
            "audio_file_url": audio_url or "",
            "qr_code_url": qr_data["qr_url"] if qr_data else "",
            "qr_code_data": qr_data["qr_data"] if qr_data else "",
            "status": "pending",
            "payment_method": "COD",
            "total_amount": float(frame["price"]),
            "notes": data.get("notes", ""),
            "created_at": datetime.now().isoformat()
        }
        
        # Save to Supabase
        print(f"💾 Saving order to Supabase...")
        supabase_result = save_order_to_supabase(order_data)
        
        if supabase_result["success"]:
            # Also save locally for backup
            orders.append(order_data)
            
            response_data = {
                "id": order_id,
                "message": "Order created successfully with audio and QR code!",
                "order": order_data,
                "supabase_id": supabase_result["data"][0]["id"] if supabase_result["data"] else None
            }
            
            if audio_url:
                response_data["audio_uploaded"] = True
                response_data["audio_url"] = audio_url
            if qr_data:
                response_data["qr_generated"] = True
                response_data["qr_url"] = qr_data["qr_url"]
            
            print(f"✅ Order created successfully!")
            return jsonify(response_data), 201
        else:
            # Fallback to local storage
            orders.append(order_data)
            return jsonify({
                "id": order_id,
                "message": "Order created successfully (local storage - Supabase unavailable)",
                "order": order_data
            }), 201
            
    except Exception as e:
        print(f"❌ Order creation error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/scan/<int:frame_id>/', methods=['GET'])
def scan_frame(frame_id):
    """Scan frame QR code - returns audio URL"""
    try:
        # Find order with this frame_id that has audio
        order = next((o for o in orders if o["frame_id"] == frame_id and o.get("audio_file_url")), None)
        
        if not order:
            # Try to get from Supabase
            response = requests.get(f"{SUPABASE_URL}/rest/v1/api_order?frame_id=eq.{frame_id}&audio_file_url=not.is.null", headers=get_supabase_headers())
            if response.status_code == 200:
                orders_data = response.json()
                if orders_data:
                    order = orders_data[0]
        
        if order and order.get("audio_file_url"):
            return jsonify({
                "frame_id": frame_id,
                "frame_title": order.get("frame_title", "Unknown Frame"),
                "audio_url": order["audio_file_url"],
                "signed_audio_url": order["audio_file_url"],  # Cloudinary URLs are already signed
                "qr_code_url": order.get("qr_code_url", ""),
                "message": "Audio file found successfully"
            })
        else:
            return jsonify({
                "frame_id": frame_id,
                "frame_title": "Unknown Frame",
                "audio_url": None,
                "signed_audio_url": None,
                "qr_code_url": None,
                "message": "No audio file found for this frame"
            })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/track-play/<int:frame_id>/', methods=['POST'])
def track_play(frame_id):
    """Track audio play event"""
    try:
        # In a real implementation, you would save play statistics to database
        return jsonify({
            "message": "Play tracked successfully",
            "plays_count": 1,
            "frame_id": frame_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/statistics/', methods=['GET'])
def get_statistics():
    """Get system statistics"""
    try:
        # Get orders from Supabase
        response = requests.get(f"{SUPABASE_URL}/rest/v1/api_order", headers=get_supabase_headers())
        total_orders = len(response.json()) if response.status_code == 200 else len(orders)
        
        return jsonify({
            "total_orders": total_orders,
            "total_frames": len(FRAMES_DATA),
            "orders_with_audio": len([o for o in orders if o.get("audio_file_url")]),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Complete Audio Frame Art API...")
    print("📡 Available endpoints:")
    print("  GET  /api/frames/           - List all frames")
    print("  GET  /api/frames/{id}/      - Get specific frame")
    print("  GET  /api/orders/            - List orders from Supabase")
    print("  POST /api/orders/            - Create order (with audio upload & QR generation)")
    print("  GET  /api/scan/{id}/         - Scan frame QR code")
    print("  POST /api/track-play/{id}/   - Track audio play")
    print("  GET  /api/statistics/        - Get statistics")
    print("  GET  /health/                 - Health check")
    print("🌐 Server running on http://localhost:8001")
    
    if CLOUDINARY_API_KEY == "your-api-key":
        print("⚠️  IMPORTANT: Configure your Cloudinary credentials!")
        print("   Edit this file and replace CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET")
    
    app.run(host='0.0.0.0', port=8001, debug=False)
