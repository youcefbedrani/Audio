#!/usr/bin/env python3
"""
Audio Frame Art API with Spotify Waveform Code Generation
Replaces QR codes with Spotify-style waveform codes
"""

import os
import json
import uuid
import base64
import requests
import numpy as np
import librosa
from datetime import datetime
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from io import BytesIO
from PIL import Image, ImageDraw

# Cloudinary imports
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

# Configuration
SUPABASE_URL = "https://qksmfogjdurxgzmlcujb.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrc21mb2dqZHVyeGd6bWxjdWpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA0NTg3OTEsImV4cCI6MjA3NjAzNDc5MX0.E1VDpkzcq3AzyPiNZOHU2_5IPyx2k76UdZZiaXg3CVk"

# Cloudinary configuration
CLOUDINARY_CLOUD_NAME = "your_cloud_name"  # Replace with your Cloudinary cloud name
CLOUDINARY_API_KEY = "your_api_key"        # Replace with your Cloudinary API key
CLOUDINARY_API_SECRET = "your_api_secret"  # Replace with your Cloudinary API secret

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
        "name": "Classic Wood Frame",
        "price": 29.99,
        "description": "Beautiful wooden frame for your audio memories",
        "image_url": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400"
    },
    {
        "id": 2,
        "name": "Modern Metal Frame",
        "price": 39.99,
        "description": "Sleek metal frame with contemporary design",
        "image_url": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400"
    },
    {
        "id": 3,
        "name": "Vintage Frame",
        "price": 49.99,
        "description": "Antique-style frame for timeless appeal",
        "image_url": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400"
    }
]

# In-memory storage for orders
orders = []

def get_supabase_headers():
    """Get headers for Supabase API calls"""
    return {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

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
            # Generate fallback waveform
            return generate_fallback_waveform(order_id)
        
        # Analyze audio waveform
        waveform_data = analyze_audio_waveform(audio_data)
        
        # Create Spotify waveform image
        waveform_image = create_spotify_waveform_image(waveform_data)
        
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
        
        # Return Cloudinary URL if available, otherwise local URL
        if cloudinary_waveform_url:
            waveform_url = cloudinary_waveform_url
            print(f"   Waveform uploaded to Cloudinary: {waveform_url}")
        else:
            waveform_url = f"http://localhost:8001/uploads/waveforms/{waveform_filename}"
            print(f"   Using local waveform URL: {waveform_url}")
        
        # Create waveform data for storage
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
        # Save audio data to temporary file
        with BytesIO(audio_data) as audio_buffer:
            # Load audio with librosa
            y, sr = librosa.load(audio_buffer, sr=None)
            
            # Calculate RMS energy for each segment (Spotify-style analysis)
            bar_count = 60  # Standard Spotify configuration
            hop_length = len(y) // bar_count
            waveform_data = []
            
            for i in range(bar_count):
                start = i * hop_length
                end = min((i + 1) * hop_length, len(y))
                segment = y[start:end]
                
                if len(segment) > 0:
                    # Calculate RMS energy and normalize
                    rms = np.sqrt(np.mean(segment**2))
                    # Apply logarithmic scaling for better visual representation
                    normalized_rms = np.log1p(rms * 10) / np.log1p(1.0)
                    normalized_rms = min(1.0, normalized_rms)
                    waveform_data.append(normalized_rms)
                else:
                    waveform_data.append(0.1)  # Minimum height
            
            return np.array(waveform_data)
            
    except Exception as e:
        print(f"⚠️  Audio analysis failed, using fallback: {e}")
        # Fallback: generate realistic waveform pattern
        return generate_realistic_waveform()

def generate_realistic_waveform():
    """Generate a realistic waveform pattern that looks like Spotify codes"""
    bar_count = 60
    x = np.linspace(0, 4 * np.pi, bar_count)
    
    # Base pattern with multiple frequency components
    base_pattern = (
        np.abs(np.sin(x)) * 0.6 +           # Main frequency
        np.abs(np.sin(x * 2)) * 0.3 +       # Harmonic
        np.abs(np.sin(x * 3)) * 0.1         # Higher harmonic
    )
    
    # Add some noise for realism
    noise = np.random.normal(0, 0.08, bar_count)
    waveform = np.clip(base_pattern + noise, 0, 1)
    
    # Add some "beats" or "peaks" to make it look more realistic
    beat_indices = np.random.choice(bar_count, size=bar_count // 6, replace=False)
    for idx in beat_indices:
        start = max(0, idx - 2)
        end = min(bar_count, idx + 3)
        waveform[start:end] = np.maximum(waveform[start:end], 
                                       np.random.uniform(0.7, 1.0, end - start))
    
    # Add some quiet sections
    quiet_indices = np.random.choice(bar_count, size=bar_count // 8, replace=False)
    for idx in quiet_indices:
        start = max(0, idx - 1)
        end = min(bar_count, idx + 2)
        waveform[start:end] = np.minimum(waveform[start:end], 
                                       np.random.uniform(0.1, 0.3, end - start))
    
    return waveform

def create_spotify_waveform_image(waveform_data):
    """Create the Spotify-style waveform code image with vertical bars"""
    width = 800
    height = 200
    bar_count = len(waveform_data)
    bar_width = 8
    bar_spacing = 4
    max_bar_height = height - 40  # Leave 20px margin top/bottom
    
    # Create white background (Spotify style)
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Calculate total width needed for bars
    total_bars_width = bar_count * (bar_width + bar_spacing) - bar_spacing
    start_x = (width - total_bars_width) // 2
    
    # Draw waveform bars (vertical bars like Spotify codes)
    for i, amplitude in enumerate(waveform_data):
        # Calculate bar height based on amplitude
        bar_height = max(4, int(amplitude * max_bar_height))
        
        # Center the bar vertically
        y_start = (height - bar_height) // 2
        y_end = y_start + bar_height
        
        # Calculate x position
        x_start = start_x + i * (bar_width + bar_spacing)
        x_end = x_start + bar_width
        
        # Draw rounded rectangle for each bar (Spotify style)
        corner_radius = min(bar_width // 2, (y_end - y_start) // 2)
        if corner_radius <= 0:
            draw.rectangle([x_start, y_start, x_end, y_end], fill='black')
        else:
            draw.rounded_rectangle([x_start, y_start, x_end, y_end], radius=corner_radius, fill='black')
    
    # Convert to bytes
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG', optimize=True)
    img_byte_arr.seek(0)
    
    return img_byte_arr.getvalue()

def generate_fallback_waveform(order_id):
    """Generate a fallback waveform when audio analysis fails"""
    try:
        print(f"🎵 Generating fallback Spotify waveform for order {order_id}")
        
        # Generate realistic waveform pattern
        waveform_data = generate_realistic_waveform()
        
        # Create waveform image
        waveform_image = create_spotify_waveform_image(waveform_data)
        
        # Save waveform locally
        waveform_dir = "uploads/waveforms"
        if not os.path.exists(waveform_dir):
            os.makedirs(waveform_dir)
        
        waveform_filename = f"spotify_waveform_{order_id}.png"
        waveform_path = os.path.join(waveform_dir, waveform_filename)
        
        with open(waveform_path, "wb") as f:
            f.write(waveform_image)
        
        print(f"✅ Fallback waveform saved: {waveform_path}")
        
        # Try to upload to Cloudinary
        cloudinary_waveform_url = upload_to_cloudinary(
            waveform_path, 
            folder="audio_frame_art/waveforms", 
            resource_type="image"
        )
        
        # Return Cloudinary URL if available, otherwise local URL
        if cloudinary_waveform_url:
            waveform_url = cloudinary_waveform_url
        else:
            waveform_url = f"http://localhost:8001/uploads/waveforms/{waveform_filename}"
        
        # Create waveform data for storage
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

def save_order_to_supabase(order_data):
    """Save order to Supabase database"""
    try:
        # Prepare data for Supabase
        supabase_data = {
            "customer_name": order_data.get("customer_name", ""),
            "customer_phone": order_data.get("customer_phone", ""),
            "customer_email": order_data.get("customer_email", ""),
            "delivery_address": order_data.get("delivery_address", ""),
            "city": order_data.get("city", ""),
            "postal_code": order_data.get("postal_code", "00000"),
            "frame_id": order_data.get("frame_id", 1),
            "status": "pending",
            "payment_method": order_data.get("payment_method", "cash"),
            "total_amount": order_data.get("total_amount", 0),
            "notes": order_data.get("notes", ""),
            "created_at": datetime.now().isoformat()
        }
        
        # Add audio and waveform fields if available
        if "audio_file_url" in order_data:
            supabase_data["audio_file_url"] = order_data["audio_file_url"]
        if "waveform_url" in order_data:
            supabase_data["qr_code_url"] = order_data["waveform_url"]  # Using qr_code_url field for waveform
        if "waveform_data" in order_data:
            supabase_data["qr_code_data"] = order_data["waveform_data"]  # Using qr_code_data field for waveform data
        
        # Send to Supabase
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/api_order",
            headers=get_supabase_headers(),
            json=supabase_data
        )
        
        if response.status_code in [200, 201]:
            print(f"✅ Order saved to Supabase successfully")
            return True
        else:
            print(f"❌ Supabase save error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Supabase save error: {e}")
        return False

# API Routes
@app.route('/api/frames/', methods=['GET'])
def get_frames():
    """Get all available frames"""
    return jsonify(FRAMES_DATA)

@app.route('/api/frames/<int:frame_id>/', methods=['GET'])
def get_frame(frame_id):
    """Get specific frame by ID"""
    frame = next((f for f in FRAMES_DATA if f["id"] == frame_id), None)
    if frame:
        return jsonify(frame)
    return jsonify({"error": "Frame not found"}), 404

@app.route('/api/orders/', methods=['GET'])
def get_orders():
    """Get all orders"""
    return jsonify(orders)

@app.route('/api/orders/', methods=['POST'])
def create_order():
    """Create a new order with Spotify waveform generation"""
    try:
        # Get form data
        order_data = request.form.to_dict()
        
        # Handle file upload
        audio_file = None
        if 'audio_file' in request.files:
            audio_file = request.files['audio_file']
        
        # Generate order ID
        order_id = len(orders) + 1
        
        # Process audio file if provided
        audio_url = None
        if audio_file and audio_file.filename:
            audio_url = save_audio_file(audio_file)
            if audio_url:
                order_data["audio_file_url"] = audio_url
                print(f"✅ Audio file processed: {audio_url}")
        
        # Generate Spotify waveform code if audio is available
        waveform_result = None
        if audio_url:
            waveform_result = generate_spotify_waveform_code(audio_url, order_id)
            if waveform_result:
                order_data["waveform_url"] = waveform_result["waveform_url"]
                order_data["waveform_data"] = waveform_result["waveform_data"]
                print(f"✅ Spotify waveform generated: {waveform_result['waveform_url']}")
        
        # Create order object
        order = {
            "id": order_id,
            "customer_name": order_data.get("customer_name", ""),
            "customer_phone": order_data.get("customer_phone", ""),
            "customer_email": order_data.get("customer_email", ""),
            "delivery_address": order_data.get("delivery_address", ""),
            "city": order_data.get("city", ""),
            "postal_code": order_data.get("postal_code", "00000"),
            "frame_id": int(order_data.get("frame_id", 1)),
            "status": "pending",
            "payment_method": order_data.get("payment_method", "cash"),
            "total_amount": float(order_data.get("total_amount", 0)),
            "notes": order_data.get("notes", ""),
            "audio_file_url": audio_url,
            "waveform_url": waveform_result["waveform_url"] if waveform_result else None,
            "waveform_data": waveform_result["waveform_data"] if waveform_result else None,
            "created_at": datetime.now().isoformat()
        }
        
        # Add to orders list
        orders.append(order)
        
        # Save to Supabase
        save_order_to_supabase(order)
        
        return jsonify(order), 201
        
    except Exception as e:
        print(f"❌ Order creation error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/scan/<int:order_id>/', methods=['GET'])
def scan_order(order_id):
    """Scan order and return audio playback info"""
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    
    return jsonify({
        "order_id": order_id,
        "audio_url": order.get("audio_file_url"),
        "waveform_url": order.get("waveform_url"),
        "waveform_type": "spotify_style",
        "status": "ready_for_playback"
    })

@app.route('/api/track-play/<int:order_id>/', methods=['POST'])
def track_play(order_id):
    """Track audio play event"""
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    
    # Update play count or timestamp
    order["last_played"] = datetime.now().isoformat()
    
    return jsonify({
        "order_id": order_id,
        "status": "play_tracked",
        "timestamp": order["last_played"]
    })

@app.route('/api/statistics/', methods=['GET'])
def get_statistics():
    """Get API statistics"""
    return jsonify({
        "total_orders": len(orders),
        "total_frames": len(FRAMES_DATA),
        "orders_with_audio": len([o for o in orders if o.get("audio_file_url")]),
        "orders_with_waveforms": len([o for o in orders if o.get("waveform_url")]),
        "waveform_type": "spotify_style",
        "cloudinary_configured": CLOUDINARY_AVAILABLE and CLOUDINARY_CLOUD_NAME != "your_cloud_name"
    })

@app.route('/health/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test Supabase connection
        response = requests.get(f"{SUPABASE_URL}/rest/v1/api_order?select=count", headers=get_supabase_headers())
        supabase_connected = response.status_code == 200
        
        # Test Cloudinary connection
        cloudinary_configured = False
        if CLOUDINARY_AVAILABLE and CLOUDINARY_CLOUD_NAME != "your_cloud_name":
            try:
                cloudinary_api.ping()
                cloudinary_configured = True
            except:
                cloudinary_configured = False
        
        return jsonify({
            "status": "healthy",
            "supabase_connected": supabase_connected,
            "supabase_url": SUPABASE_URL,
            "audio_storage": "cloudinary" if cloudinary_configured else "local",
            "waveform_generation": "spotify_style",
            "cloudinary_configured": cloudinary_configured,
            "cloudinary_available": CLOUDINARY_AVAILABLE,
            "timestamp": datetime.now().isoformat(),
            "total_orders": len(orders)
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve uploaded files with correct content type"""
    try:
        from flask import send_from_directory, Response
        import mimetypes
        
        # Determine correct content type based on file extension
        if filename.endswith('.webm'):
            mimetype = 'audio/webm'
        elif filename.endswith('.mp3'):
            mimetype = 'audio/mpeg'
        elif filename.endswith('.wav'):
            mimetype = 'audio/wav'
        elif filename.endswith('.ogg'):
            mimetype = 'audio/ogg'
        elif filename.endswith('.png'):
            mimetype = 'image/png'
        elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
            mimetype = 'image/jpeg'
        else:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        
        return send_from_directory('uploads', filename, mimetype=mimetype)
    except Exception as e:
        print(f"File serving error: {e}")
        return "File not found", 404

@app.route('/test_audio_player.html')
def test_audio_player():
    """Serve the test audio player HTML file"""
    try:
        from flask import send_file
        return send_file('test_audio_player.html', mimetype='text/html')
    except Exception as e:
        print(f"Test file serving error: {e}")
        return "Test file not found", 404

@app.route('/test_spotify_waveform.html')
def test_spotify_waveform():
    """Serve the Spotify waveform test HTML file"""
    try:
        from flask import send_file
        return send_file('test_spotify_waveform.html', mimetype='text/html')
    except Exception as e:
        print(f"Spotify waveform test file serving error: {e}")
        return "Test file not found", 404

if __name__ == '__main__':
    print("🎵 Starting Audio Frame Art API with Spotify Waveform Generation...")
    print("📡 Available endpoints:")
    print("  GET  /api/frames/           - List all frames")
    print("  GET  /api/frames/{id}/      - Get specific frame")
    print("  GET  /api/orders/            - List orders")
    print("  POST /api/orders/            - Create order with Spotify waveform")
    print("  GET  /api/scan/{id}/         - Scan order waveform")
    print("  POST /api/track-play/{id}/   - Track audio play")
    print("  GET  /api/statistics/        - Get statistics")
    print("  GET  /health/                 - Health check")
    print("🌐 Server running on http://localhost:8002")
    print("🎵 Generating Spotify-style waveform codes (NOT QR codes)")
    
    app.run(host='0.0.0.0', port=8002, debug=False)
