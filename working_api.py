#!/usr/bin/env python3
"""
Working API for Audio Frame Art
Simple and reliable API that handles orders and QR scanning
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Sample frame data
FRAMES_DATA = [
    {
        "id": 1,
        "title": "Simple Order",
        "description": "إطار خشبي أنيق مصنوع من خشب البلوط الطبيعي، مثالي للصور العائلية والذكريات الثمينة.",
        "frame_type": "simple",
        "price": 5000.00,
        "is_available": True,
        "image": "/assets/order-simple.png",
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 2,
        "title": "VIP Order",
        "description": "إطار معدني أنيق بتصميم عصري، مثالي للمكاتب والمنازل العصرية.",
        "frame_type": "vip",
        "price": 6000.00,
        "is_available": True,
        "image": "/assets/order-vip.png",
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 3,
        "title": "Handmade Order",
        "description": "إطار زجاجي شفاف أنيق، يبرز جمال الصورة دون إلهاء.",
        "frame_type": "handmade",
        "price": 7000.00,
        "is_available": True,
        "image": "/assets/order-handmade.png",
        "created_at": "2024-01-01T00:00:00Z"
    }
]

# Create upload directory
UPLOAD_FOLDER = 'uploads'
PERSISTENCE_FILE = os.path.join(UPLOAD_FOLDER, 'persistence.json')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Global data state
orders = []
audio_files = {}
# Pre-initialize statistics for all sample frames
statistics = {frame["id"]: {"scans_count": 0, "plays_count": 0, "last_scan": None, "last_play": None} for frame in FRAMES_DATA}

def save_data():
    try:
        data = {
            "orders": orders,
            "statistics": statistics,
            "audio_files": audio_files
        }
        with open(PERSISTENCE_FILE, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error saving data: {e}")

def load_data():
    global orders, statistics, audio_files
    if os.path.exists(PERSISTENCE_FILE):
        try:
            with open(PERSISTENCE_FILE, 'r') as f:
                data = json.load(f)
                orders = data.get("orders", [])
                # Update statistics, merging with defaults for any new frames
                loaded_stats = data.get("statistics", {})
                for frame_id_str, stats in loaded_stats.items():
                    try:
                        statistics[int(frame_id_str)] = stats
                    except ValueError:
                        pass
                audio_files = data.get("audio_files", {})
        except Exception as e:
            print(f"Error loading data: {e}")

# Initial load
load_data()

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
    
    # Add statistics to frame
    frame_with_stats = frame.copy()
    frame_with_stats["statistics"] = statistics.get(frame_id, {"scans_count": 0, "plays_count": 0, "last_scan": None, "last_play": None})
    
    return jsonify(frame_with_stats)

@app.route('/api/orders/', methods=['GET', 'POST'])
def handle_orders():
    """Handle orders - GET for list, POST for create"""
    if request.method == 'GET':
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
            
            # Map fields (Frontend sends wilaya/baladya, backend expects city)
            if 'city' not in data and 'baladya' in data:
                data['city'] = data['baladya']
            
            required_fields = ['customer_name', 'customer_phone', 'delivery_address']
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
            
            # Handle audio file upload
            audio_url = None
            if audio_file and hasattr(audio_file, 'filename') and audio_file.filename:
                try:
                    filename = secure_filename(audio_file.filename)
                    unique_filename = f"{uuid.uuid4()}_{filename}"
                    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                    audio_file.save(file_path)
                    audio_url = f"/uploads/{unique_filename}"
                    
                    # Store audio file info
                    audio_files[unique_filename] = {
                        "frame_id": frame_id,
                        "original_name": filename,
                        "file_path": file_path,
                        "uploaded_at": datetime.now().isoformat()
                    }
                except Exception as e:
                    print(f"Error saving audio file: {e}")
                    # Continue without audio file
            
            # Create order
            order = {
                "id": len(orders) + 1,
                "customer_name": data["customer_name"],
                "customer_phone": data["customer_phone"],
                "customer_email": data.get("customer_email", ""),
                "delivery_address": data["delivery_address"],
                "city": data["city"],
                "postal_code": data.get("postal_code", ""),
                "wilaya": data.get("wilaya", ""),
                "baladya": data.get("baladya", ""),
                "frame_id": frame_id,
                "frame": frame,
                "audio_file": audio_url,
                "status": "pending",
                "payment_method": "COD",
                "total_amount": float(frame["price"]),
                "notes": data.get("notes", ""),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            orders.append(order)
            save_data()
            
            return jsonify({
                "id": order["id"],
                "message": "Order created successfully",
                "order": order
            }), 201
            
        except Exception as e:
            print(f"Error creating order: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

@app.route('/api/audio/<int:frame_id>/', methods=['GET'])
def get_audio(frame_id):
    """Handle audio lookup"""
    frame = next((f for f in FRAMES_DATA if f["id"] == frame_id), None)
    if not frame:
        return jsonify({"error": "Frame not found"}), 404
    
    # Update statistics
    if frame_id in statistics:
        statistics[frame_id]["scans_count"] += 1
        statistics[frame_id]["last_scan"] = datetime.now().isoformat()
        save_data()
    
    # Find audio file for this frame
    audio_url = None
    for filename, audio_info in audio_files.items():
        if audio_info["frame_id"] == frame_id:
            audio_url = f"http://localhost:8001/uploads/{filename}"
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
    if frame_id in statistics:
        statistics[frame_id]["plays_count"] += 1
        statistics[frame_id]["last_play"] = datetime.now().isoformat()
        save_data()
    
    return jsonify({
        "message": "Play tracked successfully",
        "plays_count": statistics.get(frame_id, {}).get("plays_count", 0)
    })

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    from flask import send_from_directory
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/api/statistics/', methods=['GET'])
def get_statistics():
    """Get system statistics"""
    total_orders = len(orders)
    total_frames = len(FRAMES_DATA)
    total_scans = sum(stats["scans_count"] for stats in statistics.values())
    total_plays = sum(stats["plays_count"] for stats in statistics.values())
    
    return jsonify({
        "total_orders": total_orders,
        "total_frames": total_frames,
        "total_scans": total_scans,
        "total_plays": total_plays,
        "pending_orders": len([o for o in orders if o["status"] == "pending"]),
        "delivered_orders": len([o for o in orders if o["status"] == "delivered"])
    })

@app.route('/health/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    print("🚀 Starting Working API...")
    print("📡 Available endpoints:")
    print("  GET  /api/frames/           - List all frames")
    print("  GET  /api/frames/{id}/      - Get specific frame")
    print("  GET  /api/orders/            - List orders")
    print("  POST /api/orders/            - Create order")
    print("  GET  /api/audio/{id}/         - Get frame audio")
    print("  POST /api/track-play/{id}/   - Track audio play")
    print("  GET  /api/statistics/        - Get statistics")
    print("  GET  /health/                 - Health check")
    print("\n🌐 Server running on http://localhost:8001")
    
    app.run(host='0.0.0.0', port=8001, debug=True)
