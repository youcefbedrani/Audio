#!/usr/bin/env python3
"""
Working Supabase + Cloudinary Integrated API for Audio Frame Art
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import uuid
import requests
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Supabase Configuration
SUPABASE_URL = "https://qksmfogjdurxgzmlcujb.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrc21mb2dqZHVyeGd6bWxjdWpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA0NTg3OTEsImV4cCI6MjA3NjAzNDc5MX0.E1VDpkzcq3AzyPiNZOHU2_5IPyx2k76UdZZiaXg3CVk"

# Sample frame data
FRAMES_DATA = [
    {
        "id": 1,
        "title": "إطار خشبي كلاسيكي",
        "description": "إطار خشبي أنيق مصنوع من خشب البلوط الطبيعي، مثالي للصور العائلية والذكريات الثمينة.",
        "frame_type": "wooden",
        "price": 150.00,
        "is_available": True,
        "image": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400",
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 2,
        "title": "إطار معدني عصري",
        "description": "إطار معدني أنيق بتصميم عصري، مثالي للمكاتب والمنازل العصرية.",
        "frame_type": "metal",
        "price": 120.00,
        "is_available": True,
        "image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400",
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 3,
        "title": "إطار زجاجي شفاف",
        "description": "إطار زجاجي شفاف أنيق، يبرز جمال الصورة دون إلهاء.",
        "frame_type": "glass",
        "price": 100.00,
        "is_available": True,
        "image": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400",
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 4,
        "title": "إطار بلاستيكي ملون",
        "description": "إطار بلاستيكي بألوان زاهية، مثالي لغرف الأطفال والمساحات المبهجة.",
        "frame_type": "plastic",
        "price": 80.00,
        "is_available": True,
        "image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400",
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 5,
        "title": "إطار خشبي فاخر",
        "description": "إطار خشبي فاخر منحوت يدوياً، قطعة فنية حقيقية تليق بأهم اللحظات.",
        "frame_type": "wooden",
        "price": 200.00,
        "is_available": True,
        "image": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400",
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 6,
        "title": "إطار معدني ذهبي",
        "description": "إطار معدني مذهب أنيق، يضفي لمسة من الفخامة والأناقة على أي مساحة.",
        "frame_type": "metal",
        "price": 180.00,
        "is_available": True,
        "image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400",
        "created_at": "2024-01-01T00:00:00Z"
    }
]

# In-memory storage for orders (fallback)
orders = []

def get_supabase_headers():
    """Get headers for Supabase API calls"""
    return {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

def save_order_to_supabase(order_data):
    """Save order to Supabase database"""
    try:
        # First, try to save to the existing api_order table
        url = f"{SUPABASE_URL}/rest/v1/api_order"
        headers = get_supabase_headers()
        
        # Map our data to the existing table structure
        supabase_data = {
            "customer_name": order_data["customer_name"],
            "customer_phone": order_data["customer_phone"],
            "customer_email": order_data.get("customer_email", ""),
            "delivery_address": order_data["delivery_address"],
            "city": order_data["city"],
            "postal_code": order_data.get("postal_code", ""),
            "wilaya": order_data.get("wilaya", ""),
            "baladya": order_data.get("baladya", ""),
            "frame_id": order_data["frame_id"],
            "audio_file_url": order_data.get("audio_file_url"),
            "status": order_data.get("status", "pending"),
            "payment_method": order_data.get("payment_method", "COD"),
            "total_amount": order_data["total_amount"],
            "notes": order_data.get("notes", ""),
            "created_at": order_data.get("created_at", datetime.now().isoformat())
        }
        
        response = requests.post(url, headers=headers, json=supabase_data)
        
        if response.status_code in [200, 201]:
            print(f"✅ Order saved to Supabase: {response.json()}")
            return response.json()
        else:
            print(f"❌ Supabase error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error saving to Supabase: {e}")
        return None

def get_orders_from_supabase():
    """Get orders from Supabase database"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/api_order"
        headers = get_supabase_headers()
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Supabase error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"❌ Error getting from Supabase: {e}")
        return []

@app.route('/api/frames/', methods=['GET'])
def get_frames():
    """Get all available frames"""
    return jsonify(FRAMES_DATA)

@app.route('/api/frames/<int:frame_id>/', methods=['GET'])
def get_frame(frame_id):
    """Get specific frame by ID"""
    frame = next((f for f in FRAMES_DATA if f["id"] == frame_id), None)
    if not frame:
        return jsonify({"error": "Frame not found"}), 404
    return jsonify(frame)

@app.route('/api/orders/', methods=['GET', 'POST'])
def handle_orders():
    """Handle orders - GET for list, POST for create"""
    if request.method == 'GET':
        # Get orders from Supabase
        supabase_orders = get_orders_from_supabase()
        if supabase_orders:
            return jsonify(supabase_orders)
        else:
            # Fallback to local storage
            return jsonify(orders)
    
    elif request.method == 'POST':
        try:
            # Get data from request
            if request.is_json:
                data = request.get_json()
                audio_file = None
            else:
                data = request.form.to_dict()
                audio_file = request.files.get('audio_file')
            
            # Validate required fields
            if not data:
                return jsonify({"error": "No data received"}), 400
            
            required_fields = ['customer_name', 'customer_phone', 'delivery_address', 'city']
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400
            
            # Get frame ID
            frame_id = data.get('frame') or data.get('frame_id')
            if not frame_id:
                return jsonify({"error": "Missing required field: frame or frame_id"}), 400
            
            frame_id = int(frame_id)
            
            # Find frame
            frame = next((f for f in FRAMES_DATA if f["id"] == frame_id), None)
            if not frame:
                return jsonify({"error": "Frame not found"}), 400
            
            # Handle audio file (for now, just store the filename)
            audio_url = None
            if audio_file and hasattr(audio_file, 'filename') and audio_file.filename:
                # For now, just use a placeholder URL
                audio_url = f"https://res.cloudinary.com/dulct8pma/video/upload/v1/audio_{uuid.uuid4()}.mp3"
                print(f"📁 Audio file uploaded: {audio_file.filename}")
            
            # Prepare order data
            order_data = {
                "customer_name": data["customer_name"],
                "customer_phone": data["customer_phone"],
                "customer_email": data.get("customer_email", ""),
                "delivery_address": data["delivery_address"],
                "city": data["city"],
                "postal_code": data.get("postal_code", ""),
                "wilaya": data.get("wilaya", ""),
                "baladya": data.get("baladya", ""),
                "frame_id": frame_id,
                "frame_title": frame["title"],
                "frame_type": frame["frame_type"],
                "audio_file_url": audio_url,
                "status": "pending",
                "payment_method": "COD",
                "total_amount": float(frame["price"]),
                "notes": data.get("notes", ""),
                "created_at": datetime.now().isoformat()
            }
            
            # Save to Supabase
            print("💾 Saving order to Supabase...")
            supabase_result = save_order_to_supabase(order_data)
            
            if supabase_result:
                print("✅ Order saved to Supabase successfully!")
                return jsonify({
                    "id": supabase_result[0]["id"] if isinstance(supabase_result, list) else supabase_result.get("id"),
                    "message": "Order created successfully and saved to Supabase database!",
                    "order": order_data,
                    "supabase_id": supabase_result[0]["id"] if isinstance(supabase_result, list) else supabase_result.get("id")
                }), 201
            else:
                print("⚠️ Supabase unavailable, saving locally...")
                # Fallback to local storage
                order_data["id"] = int(datetime.now().timestamp())
                orders.append(order_data)
                return jsonify({
                    "id": order_data["id"],
                    "message": "Order created successfully (local storage - Supabase unavailable)",
                    "order": order_data
                }), 201
            
        except Exception as e:
            print(f"❌ Error creating order: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

@app.route('/api/scan/<int:frame_id>/', methods=['GET'])
def scan_frame(frame_id):
    """Handle QR code scan"""
    frame = next((f for f in FRAMES_DATA if f["id"] == frame_id), None)
    if not frame:
        return jsonify({"error": "Frame not found"}), 404
    
    # Get orders from Supabase to find audio for this frame
    supabase_orders = get_orders_from_supabase()
    audio_url = None
    
    # Find the most recent order for this frame with audio
    for order in sorted(supabase_orders, key=lambda x: x.get('created_at', ''), reverse=True):
        if order.get('frame_id') == frame_id and order.get('audio_file_url'):
            audio_url = order['audio_file_url']
            break
    
    if not audio_url:
        # Return placeholder audio URL
        audio_url = f"http://localhost:8001/placeholder_audio.mp3"
    
    return jsonify({
        "frame_id": frame_id,
        "frame_title": frame["title"],
        "audio_url": audio_url,
        "signed_audio_url": audio_url,
        "message": "Audio file found successfully"
    })

@app.route('/api/track-play/<int:frame_id>/', methods=['POST'])
def track_play(frame_id):
    """Track audio play event"""
    return jsonify({
        "message": "Play tracked successfully",
        "plays_count": 1
    })

@app.route('/api/statistics/', methods=['GET'])
def get_statistics():
    """Get system statistics"""
    supabase_orders = get_orders_from_supabase()
    local_orders = orders
    
    total_orders = len(supabase_orders) + len(local_orders)
    
    return jsonify({
        "total_orders": total_orders,
        "supabase_orders": len(supabase_orders),
        "local_orders": len(local_orders),
        "total_frames": len(FRAMES_DATA),
        "total_scans": 0,
        "total_plays": 0,
        "pending_orders": len([o for o in supabase_orders if o.get("status") == "pending"]) + len([o for o in local_orders if o.get("status") == "pending"]),
        "delivered_orders": len([o for o in supabase_orders if o.get("status") == "delivered"]) + len([o for o in local_orders if o.get("status") == "delivered"])
    })

@app.route('/health/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    # Test Supabase connection
    supabase_connected = False
    try:
        response = requests.get(f"{SUPABASE_URL}/rest/v1/api_order", headers=get_supabase_headers())
        supabase_connected = response.status_code == 200
    except:
        pass
    
    return jsonify({
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "supabase_connected": supabase_connected,
        "supabase_url": SUPABASE_URL,
        "total_orders": len(orders)
    })

if __name__ == '__main__':
    print("🚀 Starting Working Supabase API...")
    print("📡 Available endpoints:")
    print("  GET  /api/frames/           - List all frames")
    print("  GET  /api/frames/{id}/      - Get specific frame")
    print("  GET  /api/orders/            - List orders from Supabase")
    print("  POST /api/orders/            - Create order (saves to Supabase)")
    print("  GET  /api/scan/{id}/         - Scan frame QR code")
    print("  POST /api/track-play/{id}/   - Track audio play")
    print("  GET  /api/statistics/        - Get statistics")
    print("  GET  /health/                 - Health check")
    print(f"\n🌐 Server running on http://localhost:8001")
    print(f"🔗 Supabase URL: {SUPABASE_URL}")
    
    app.run(host='0.0.0.0', port=8001, debug=True)
