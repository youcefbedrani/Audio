#!/usr/bin/env python3
"""
Working Audio Frame Art API with Local PostgreSQL and Spotify Waveform Generation
"""

import os
import json
import uuid
import base64
import requests
import numpy as np
import librosa
import psycopg2
import sys
import traceback
from psycopg2.extras import RealDictCursor
from datetime import datetime
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from werkzeug.utils import secure_filename
from io import BytesIO
from decimal import Decimal
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
CORS(app)
try:
    import cloudinary
    import cloudinary.uploader
    from cloudinary import api as cloudinary_api
    CLOUDINARY_AVAILABLE = True
except ImportError:
    CLOUDINARY_AVAILABLE = False
    print("⚠️  Cloudinary not available. Install with: pip install cloudinary")

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration from environment variables
DB_NAME = os.getenv("DB_NAME", "audio_art")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "local_password")
DB_HOST = os.getenv("DB_HOST", "db")
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "dulct8pma")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "your_api_key")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "your_api_secret")

# Configure Cloudinary if available
if CLOUDINARY_AVAILABLE:
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET
    )

# Sample frames data
FRAMES_DATA = [
    {
        "id": 1,
        "title": "Simple Order",
        "description": "إطار خشبي أنيق مصنوع من خشب البلوط الطبيعي، مثالي للصور العائلية والذكريات الثمينة.",
        "frame_type": "simple",
        "price": 5000.00,
        "is_available": True,
        "image": "/assets/order-simple.png"
    },
    {
        "id": 2,
        "title": "VIP Order",
        "description": "إطار معدني أنيق بتصميم عصري، مثالي للمكاتب والمنازل العصرية.",
        "frame_type": "vip",
        "price": 6000.00,
        "is_available": True,
        "image": "/assets/order-vip.png"
    },
    {
        "id": 3,
        "title": "Handmade Order",
        "description": "إطار زجاجي شفاف أنيق، يبرز جمال الصورة دون إلهاء.",
        "frame_type": "handmade",
        "price": 7000.00,
        "is_available": True,
        "image": "/assets/order-handmade.png"
    }
]

def get_db_connection():
    """Connect to the PostgreSQL database server"""
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

def init_db():
    """Initialize database tables"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Create orders table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS api_order (
                id SERIAL PRIMARY KEY,
                customer_name TEXT NOT NULL,
                customer_phone TEXT NOT NULL,
                customer_email TEXT,
                delivery_address TEXT NOT NULL,
                city TEXT NOT NULL,
                postal_code TEXT,
                wilaya TEXT,
                baladya TEXT,
                frame_id INTEGER NOT NULL,
                frame_title TEXT,
                frame_type TEXT,
                audio_file_url TEXT,
                qr_code_url TEXT,
                qr_code_data TEXT,
                status TEXT DEFAULT 'pending',
                payment_method TEXT DEFAULT 'COD',
                total_amount NUMERIC(10, 2),
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                scan_id TEXT UNIQUE
            );
        """)
        
        conn.commit()
        
        # Add confirmation_agent column if it doesn't exist
        try:
            cur = conn.cursor()
            cur.execute("ALTER TABLE api_order ADD COLUMN confirmation_agent TEXT;")
            conn.commit()
            print("✅ Added confirmation_agent column")
        except Exception as e:
            conn.rollback()
            # Ignore duplicate column error
            pass
            
        # Create confirmation_agents table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS confirmation_agents (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("✅ confirmation_agents table verified")
            
        cur.close()
        conn.close()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️  Database initialization failed: {e}")

def upload_to_cloudinary(file_path, folder="audio_frame_art", resource_type="auto"):
    """Upload file to Cloudinary and return URL"""
    try:
        if not CLOUDINARY_AVAILABLE:
            print("⚠️  Cloudinary not available, using local storage")
            return None
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            file_path,
            folder=folder,
            resource_type=resource_type,
            use_filename=True,
            unique_filename=True
        )
        
        cloudinary_url = result['secure_url']
        print(f"✅ File uploaded to Cloudinary: {cloudinary_url}")
        return cloudinary_url
        
    except Exception as e:
        print(f"❌ Cloudinary upload error: {e}")
        return None

def save_audio_file(audio_file):
    """Save audio file locally and upload to Cloudinary"""
    try:
        if not audio_file or not hasattr(audio_file, 'filename') or not audio_file.filename:
            return None
        
        # Create uploads directory if it doesn't exist
        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        # Generate unique filename
        filename = f"audio_{uuid.uuid4()}_{secure_filename(audio_file.filename)}"
        file_path = os.path.join(upload_dir, filename)
        
        # Save file locally
        audio_file.save(file_path)
        print(f"✅ Audio file saved locally: {file_path}")
        
        # Try to upload to Cloudinary
        cloudinary_url = upload_to_cloudinary(file_path, folder="audio_frame_art/audio", resource_type="video")
        
        # Return Cloudinary URL if available, otherwise local URL
        if cloudinary_url:
            return cloudinary_url
        else:
            # We assume the container/localhost environment, so this URL should be reachable
            # Ideally use an environment variable for BASE_URL
            local_url = f"http://localhost:8001/uploads/{filename}"
            print(f"   Using local URL: {local_url}")
            return local_url
            
    except Exception as e:
        print(f"❌ Audio save error: {e}")
        return None

def generate_spotify_waveform_code(audio_url, order_id):
    """Generate Spotify-style waveform code for audio URL and upload to Cloudinary"""
    try:
        print(f"🎵 Generating Spotify waveform code for order {order_id}")
        
        # Download audio file
        try:
            response = requests.get(audio_url, timeout=30)
            response.raise_for_status()
            audio_data = response.content
            print(f"✅ Downloaded audio file: {len(audio_data)} bytes")
        except Exception as e:
            print(f"❌ Failed to download audio: {e}")
            return generate_fallback_waveform(order_id)
        
        # Analyze audio waveform
        waveform_data = analyze_audio_waveform(audio_data)
        
        # Create Spotify waveform image
        waveform_image = create_spotify_waveform_image(waveform_data, order_id)
        
        # Save waveform locally
        waveform_dir = "uploads/waveforms"
        if not os.path.exists(waveform_dir):
            os.makedirs(waveform_dir)
        
        waveform_filename = f"spotify_waveform_{order_id}.png"
        waveform_path = os.path.join(waveform_dir, waveform_filename)
        
        with open(waveform_path, "wb") as f:
            f.write(waveform_image)
        
        print(f"✅ Spotify waveform saved locally: {waveform_path}")
        
        # Try to upload to Cloudinary
        cloudinary_waveform_url = upload_to_cloudinary(
            waveform_path, 
            folder="audio_frame_art/waveforms", 
            resource_type="image"
        )
        
        if cloudinary_waveform_url:
            waveform_url = cloudinary_waveform_url
            print(f"   Waveform uploaded to Cloudinary: {waveform_url}")
        else:
            waveform_url = f"http://localhost:8001/uploads/waveforms/{waveform_filename}"
            print(f"   Using local waveform URL: {waveform_url}")
        
        waveform_data_json = {
            "type": "spotify_waveform",
            "order_id": order_id,
            "audio_url": audio_url,
            "waveform_url": waveform_url,
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "waveform_url": waveform_url,
            "waveform_data": json.dumps(waveform_data_json)
        }
        
    except Exception as e:
        print(f"❌ Spotify waveform generation error: {e}")
        return generate_fallback_waveform(order_id)

def analyze_audio_waveform(audio_data):
    """Analyze audio data and extract waveform information using librosa"""
    try:
        with BytesIO(audio_data) as audio_buffer:
            y, sr = librosa.load(audio_buffer, sr=None)
            
            bar_count = 60 
            hop_length = len(y) // bar_count
            waveform_data = []
            
            for i in range(bar_count):
                start = i * hop_length
                end = min((i + 1) * hop_length, len(y))
                segment = y[start:end]
                
                if len(segment) > 0:
                    rms = np.sqrt(np.mean(segment**2))
                    normalized_rms = np.log1p(rms * 10) / np.log1p(1.0)
                    normalized_rms = min(1.0, normalized_rms)
                    waveform_data.append(normalized_rms)
                else:
                    waveform_data.append(0.1)
            
            return np.array(waveform_data)
            
    except Exception as e:
        print(f"⚠️  Audio analysis failed, using fallback: {e}")
        return generate_realistic_waveform()

def generate_realistic_waveform():
    """Generate a realistic waveform pattern"""
    bar_count = 60
    x = np.linspace(0, 4 * np.pi, bar_count)
    
    base_pattern = (
        np.abs(np.sin(x)) * 0.6 +
        np.abs(np.sin(x * 2)) * 0.3 +
        np.abs(np.sin(x * 3)) * 0.1
    )
    
    noise = np.random.normal(0, 0.08, bar_count)
    waveform = np.clip(base_pattern + noise, 0, 1)
    return waveform

def create_spotify_waveform_image(waveform_data, scan_id=str):
    """Create the Spotify-style waveform code image with vertical bars and ID text"""
    width = 800
    height = 320 # Increased height
    bar_count = len(waveform_data)
    bar_width = 8
    bar_spacing = 4
    max_bar_height = 140 # Fixed bar height area
    
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    total_bars_width = bar_count * (bar_width + bar_spacing) - bar_spacing
    start_x = (width - total_bars_width) // 2
    
    # Draw bars centered vertically in the upper portion
    bars_y_center = 120
    
    for i, amplitude in enumerate(waveform_data):
        bar_height = max(4, int(amplitude * max_bar_height))
        y_start = bars_y_center - (bar_height // 2)
        y_end = y_start + bar_height
        x_start = start_x + i * (bar_width + bar_spacing)
        x_end = x_start + bar_width
        
        corner_radius = min(bar_width // 2, (y_end - y_start) // 2)
        if corner_radius <= 0:
             draw.rectangle([x_start, y_start, x_end, y_end], fill='black')
        else:
             draw.rounded_rectangle([x_start, y_start, x_end, y_end], radius=corner_radius, fill='black')
    
    try:
        # Try to load a nice large font
        font_size = 48
        try:
            # Common path for DejaVuSans on Debian/Ubuntu (after installing fonts-dejavu-core)
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except OSError:
            try:
                # Fallback to plain Sans
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
            except OSError:
                # Fallback to default if fails
                print("⚠️ Could not load TTF font, using default")
                font = ImageFont.load_default()

        text = str(scan_id)
        
        # Calculate text size for centering
        if hasattr(draw, 'textbbox'):
            left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
            text_w = right - left
            text_h = bottom - top
        else:
            # Fallback for older Pillow
            text_w, text_h = draw.textsize(text, font=font)
            
        text_x = (width - text_w) // 2
        text_y = height - 80 # Position near bottom
        
        draw.text((text_x, text_y), text, fill='black', font=font)
    except Exception as e:
        print(f"⚠️ Error drawing text: {e}")
    
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG', optimize=True)
    img_byte_arr.seek(0)
    
    return img_byte_arr.getvalue()

def generate_fallback_waveform(order_id):
    """Generate a fallback waveform when audio analysis fails"""
    try:
        print(f"🎵 Generating fallback Spotify waveform for order {order_id}")
        
        waveform_data = generate_realistic_waveform()
        waveform_image = create_spotify_waveform_image(waveform_data, order_id)
        
        waveform_dir = "uploads/waveforms"
        if not os.path.exists(waveform_dir):
            os.makedirs(waveform_dir)
        
        waveform_filename = f"spotify_waveform_{order_id}.png"
        waveform_path = os.path.join(waveform_dir, waveform_filename)
        
        with open(waveform_path, "wb") as f:
            f.write(waveform_image)
        
        print(f"✅ Fallback waveform saved: {waveform_path}")
        
        cloudinary_waveform_url = upload_to_cloudinary(
            waveform_path, 
            folder="audio_frame_art/waveforms", 
            resource_type="image"
        )
        
        if cloudinary_waveform_url:
            waveform_url = cloudinary_waveform_url
        else:
            waveform_url = f"http://localhost:8001/uploads/waveforms/{waveform_filename}"
        
        waveform_data_json = {
            "type": "spotify_waveform_fallback",
            "order_id": order_id,
            "waveform_url": waveform_url,
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "waveform_url": waveform_url,
            "waveform_data": json.dumps(waveform_data_json)
        }
        
    except Exception as e:
        print(f"❌ Fallback waveform generation error: {e}")
        return None

def save_order_to_db(order_data):
    """Save order to PostgreSQL database"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO api_order (
                customer_name, customer_phone, customer_email, delivery_address,
                city, postal_code, wilaya, baladya, frame_id, frame_title, 
                frame_type, audio_file_url, qr_code_url, qr_code_data, 
                status, payment_method, total_amount, notes, scan_id
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING id;
        """, (
            order_data["customer_name"],
            order_data["customer_phone"],
            order_data.get("customer_email", ""),
            order_data["delivery_address"],
            order_data["city"],
            order_data.get("postal_code", "00000"),
            order_data.get("wilaya", ""),
            order_data.get("baladya", ""),
            order_data["frame_id"],
            order_data["frame_title"],
            order_data["frame_type"],
            order_data.get("audio_file_url", ""),
            order_data.get("qr_code_url", ""),
            order_data.get("qr_code_data", ""),
            order_data.get("status", "pending"),
            order_data.get("payment_method", "COD"),
            order_data["total_amount"],
            order_data.get("notes", ""),
            order_data["scan_id"]
        ))
        
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        
        order_data["id"] = new_id
        print(f"✅ Order saved to Database with ID: {new_id}")
        return {"success": True, "data": order_data}
            
    except Exception as e:
        print(f"❌ Database save error: {e}")
        return {"success": False, "error": str(e)}

@app.route('/health/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.close()
        conn.close()
        db_connected = True
    except Exception as e:
        db_connected = False
        print(f"DB Check Failed: {e}")
        
    return jsonify({
        "status": "healthy",
        "database_connected": db_connected,
        "audio_storage": "cloudinary" if CLOUDINARY_AVAILABLE else "local",
        "timestamp": datetime.now().isoformat()
    })

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
    """Get orders with pagination"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 30))
        offset = (page - 1) * limit
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get total count
        cur.execute("SELECT COUNT(*) FROM api_order")
        total_orders = cur.fetchone()['count']
        
        # Get paginated orders
        cur.execute("""
            SELECT * FROM api_order 
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """, (limit, offset))
        
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        # Convert Decimal to float
        orders = []
        for row in rows:
            order_dict = dict(row)
            for key, value in order_dict.items():
                if isinstance(value, Decimal):
                    order_dict[key] = float(value)
            orders.append(order_dict)
            
        return jsonify({
            "orders": orders,
            "total": total_orders,
            "page": page,
            "limit": limit,
            "total_pages": -(-total_orders // limit) # Ceiling division
        })
    except Exception as e:
        print("ERROR IN GET_ORDERS:", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Delete an order"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if exists
        cur.execute("SELECT id FROM api_order WHERE id = %s", (order_id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({"error": "Order not found"}), 404
            
        cur.execute("DELETE FROM api_order WHERE id = %s", (order_id,))
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"success": True, "message": "Order deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """Update order details (general update)"""
    try:
        data = request.json
        allowed_fields = [
            'customer_name', 'customer_phone', 'delivery_address', 
            'wilaya', 'baladya', 'notes', 'status', 'total_amount'
        ]
        
        updates = []
        values = []
        
        for field in allowed_fields:
            if field in data:
                updates.append(f"{field} = %s")
                values.append(data[field])
                
        if not updates:
            return jsonify({"error": "No valid fields to update"}), 400
            
        values.append(order_id)
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        sql = f"UPDATE api_order SET {', '.join(updates)} WHERE id = %s RETURNING *"
        cur.execute(sql, tuple(values))
        updated_order = cur.fetchone()
        
        conn.commit()
        cur.close()
        conn.close()
        
        if not updated_order:
             return jsonify({"error": "Order not found"}), 404

        # Decimal handling
        result = dict(updated_order)
        for key, value in result.items():
            if isinstance(value, Decimal):
                result[key] = float(value)
                
        return jsonify(result)
        
    except Exception as e:
        print(f"Update error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders/', methods=['POST'])
def create_order():
    """Create new order with audio upload and QR code generation"""
    try:
        print(f"\n🆕 New order request received")
        data = request.form.to_dict()
        
        # Validation
        required_fields = ["customer_name", "customer_phone", "delivery_address", "wilaya"]
        # Basic mapping for validation
        mapped_data = {
            "customer_name": data.get("customer_name") or (data.get("first_name", "") + " " + data.get("last_name", "")).strip(),
            "customer_phone": data.get("customer_phone") or data.get("phone", ""),
            "delivery_address": data.get("delivery_address") or data.get("address", ""),
            "wilaya": data.get("wilaya", "") or data.get("city", "") # city/wilaya overlap in usage
        }
        
        # If any mapped field is empty, return error (simplified)
        if not mapped_data["customer_name"]: return jsonify({"error": "Missing customer_name"}), 400
        
        frame_id = data.get('frame') or data.get('frame_id')
        if not frame_id: return jsonify({"error": "Missing frame_id"}), 400
        
        frame_id = int(frame_id)
        frame = next((f for f in FRAMES_DATA if f["id"] == frame_id), None)
        if not frame: return jsonify({"error": "Frame not found"}), 404
        
        # Audio Processing
        audio_url = None
        waveform_data = None
        scan_id = uuid.uuid4().hex[:15].upper()
        
        if 'audio' in request.files: # Changed from 'audio_file' to 'audio' to match frontend usually, checking both
             audio_file = request.files.get('audio') or request.files.get('audio_file')
             if audio_file and audio_file.filename:
                print(f"📁 Processing audio file: {audio_file.filename}")
                audio_url = save_audio_file(audio_file)
        
        if audio_url:
            print(f"🎵 Generating Spotify waveform...")
            waveform_data = generate_spotify_waveform_code(audio_url, scan_id)
            
        # Prepare Data
        order_data = {
            "customer_name": mapped_data["customer_name"],
            "customer_phone": mapped_data["customer_phone"],
            "customer_email": data.get("customer_email", ""),
            "delivery_address": mapped_data["delivery_address"],
            "city": data.get("city") or data.get("baladiya", "") or mapped_data["wilaya"],
            "postal_code": data.get("postal_code", "00000"),
            "wilaya": mapped_data["wilaya"],
            "baladya": data.get("baladya", ""),
            "frame_id": frame_id,
            "frame_title": frame["title"],
            "frame_type": frame["frame_type"],
            "audio_file_url": audio_url or "",
            "qr_code_url": waveform_data["waveform_url"] if waveform_data else "",
            "qr_code_data": waveform_data["waveform_data"] if waveform_data else "",
            "total_amount": float(frame["price"]),
            "notes": data.get("notes", ""),
            "scan_id": scan_id
        }
        
        # Save to DB
        result = save_order_to_db(order_data)
        
        if result["success"]:
            return jsonify({
                "success": True,
                "order_id": scan_id, # Return scan_id as reference
                "db_id": result["data"]["id"],
                "message": "Order created successfully",
                "qr_code_url": order_data["qr_code_url"]
            }), 201
        else:
            return jsonify({"error": "Database save failed"}), 500
            
    except Exception as e:
        print(f"❌ Order creation error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/confirmation-agents/', methods=['GET', 'POST'])
def handle_confirmation_agents():
    """Manage confirmation agents"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        if request.method == 'GET':
            cur.execute("SELECT name FROM confirmation_agents ORDER BY name")
            rows = cur.fetchall()
            agents = [row['name'] for row in rows]
            cur.close()
            conn.close()
            return jsonify(agents)
            
        elif request.method == 'POST':
            data = request.json
            name = data.get('name')
            if not name:
                cur.close()
                conn.close()
                return jsonify({"error": "Name is required"}), 400
                
            try:
                cur.execute("INSERT INTO confirmation_agents (name) VALUES (%s) RETURNING name", (name,))
                conn.commit()
                cur.close()
                conn.close()
                return jsonify({"success": True, "name": name})
            except psycopg2.errors.UniqueViolation:
                conn.rollback()
                cur.close()
                conn.close()
                return jsonify({"success": True, "name": name, "message": "Agent already exists"})
                
    except Exception as e:
        print(f"❌ Error managing agents: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/scan/<scan_id>/', methods=['GET'])
def scan_frame(scan_id):
    """Scan frame QR code or Waveform ID - returns audio URL"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Try finding by scan_id
        cur.execute("SELECT * FROM api_order WHERE scan_id = %s", (scan_id,))
        order = cur.fetchone()
        
        # Fallback: finding by ID if numeric
        if not order and str(scan_id).isdigit():
             cur.execute("SELECT * FROM api_order WHERE id = %s", (int(scan_id),))
             order = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if order and order.get("audio_file_url"):
            return jsonify({
                "frame_id": order["frame_id"],
                "scan_id": order["scan_id"],
                "frame_title": order["frame_title"],
                "audio_url": order["audio_file_url"],
                "signed_audio_url": order["audio_file_url"],
                "message": "Audio file found successfully"
            })
        else:
            return jsonify({
                "message": "No audio file found",
                "audio_url": None
            }), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update order status and confirmation agent"""
    try:
        data = request.json
        new_status = data.get('status')
        confirmation_agent = data.get('confirmation_agent')
        
        if not new_status:
            return jsonify({"error": "Status is required"}), 400

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Check if order exists
        cur.execute("SELECT * FROM api_order WHERE id = %s", (order_id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({"error": "Order not found"}), 404

        # Update order
        if confirmation_agent:
            cur.execute("""
                UPDATE api_order 
                SET status = %s, confirmation_agent = %s 
                WHERE id = %s
                RETURNING *
            """, (new_status, confirmation_agent, order_id))
        else:
            cur.execute("""
                UPDATE api_order 
                SET status = %s 
                WHERE id = %s
                RETURNING *
            """, (new_status, order_id))
            
        updated_order = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        # Handle Decimal serialization for the response
        updated_order_dict = dict(updated_order)
        for key, value in updated_order_dict.items():
            if isinstance(value, Decimal):
                updated_order_dict[key] = float(value)
                
        return jsonify(updated_order_dict)

    except Exception as e:
        print(f"❌ Status update error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    from flask import send_from_directory
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
    print("🚀 Starting Audio API with Local PostgreSQL...")
    init_db()
    app.run(host='0.0.0.0', port=8001)
