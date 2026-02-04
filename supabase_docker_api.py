#!/usr/bin/env python3
"""
Supabase + Cloudinary Integrated API for Audio Frame Art
Optimized for Docker deployment
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
import uuid
import requests
import numpy as np
import librosa
from datetime import datetime
from werkzeug.utils import secure_filename
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import socket
import qrcode
from urllib.parse import urlparse

# Cloudinary imports
try:
    import cloudinary
    import cloudinary.uploader
    from cloudinary import api as cloudinary_api
    CLOUDINARY_AVAILABLE = True
except ImportError:
    CLOUDINARY_AVAILABLE = False
    print("⚠️  Cloudinary not available. Install with: pip install cloudinary")

# Supabase Storage imports
try:
    from supabase import create_client, Client
    SUPABASE_STORAGE_AVAILABLE = True
except ImportError:
    SUPABASE_STORAGE_AVAILABLE = False
    # Create a dummy Client type for type hints when supabase is not available
    from typing import Any
    Client = Any
    print("⚠️  Supabase Storage not available. Install with: pip install supabase")

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://qksmfogjdurxgzmlcujb.supabase.co")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrc21mb2dqZHVyeGd6bWxjdWpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA0NTg3OTEsImV4cCI6MjA3NjAzNDc5MX0.E1VDpkzcq3AzyPiNZOHU2_5IPyx2k76UdZZiaXg3CVk")

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "doszhdiv2")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "716334228474532")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "_c8BPVO91kKlb52rx4kLgTgeaL0")

# Configure Cloudinary if available
if CLOUDINARY_AVAILABLE:
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET
    )

# Sample frame data
FRAMES_DATA = [
    {
        "id": 1,
        "title": "إطار خشبي كلاسيكي",
        "description": "إطار خشبي أنيق مصنوع من خشب البلوط الطبيعي، مثالي للصور العائلية والذكريات الثمينة.",
        "frame_type": "wooden",
        "price": 3500.00,
        "is_available": True,
        "image": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400",
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 2,
        "title": "إطار معدني عصري",
        "description": "إطار معدني أنيق بتصميم عصري، مثالي للمكاتب والمنازل العصرية.",
        "frame_type": "metal",
        "price": 3500.00,
        "is_available": True,
        "image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400",
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 3,
        "title": "إطار زجاجي شفاف",
        "description": "إطار زجاجي شفاف أنيق، يبرز جمال الصورة دون إلهاء.",
        "frame_type": "glass",
        "price": 3500.00,
        "is_available": True,
        "image": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400",
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 4,
        "title": "إطار بلاستيكي ملون",
        "description": "إطار بلاستيكي بألوان زاهية، مثالي لغرف الأطفال والمساحات المبهجة.",
        "frame_type": "plastic",
        "price": 3500.00,
        "is_available": True,
        "image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400",
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 5,
        "title": "إطار خشبي فاخر",
        "description": "إطار خشبي فاخر منحوت يدوياً، قطعة فنية حقيقية تليق بأهم اللحظات.",
        "frame_type": "wooden",
        "price": 3500.00,
        "is_available": True,
        "image": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400",
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 6,
        "title": "إطار معدني ذهبي",
        "description": "إطار معدني مذهب أنيق، يضفي لمسة من الفخامة والأناقة على أي مساحة.",
        "frame_type": "metal",
        "price": 3500.00,
        "is_available": True,
        "image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400",
        "created_at": "2024-01-01T00:00:00Z"
    }
]

# In-memory storage for orders (fallback)
orders = []
PERSISTENCE_FILE = "orders_persistence.json"

def load_orders_locally():
    global orders
    if os.path.exists(PERSISTENCE_FILE):
        try:
            with open(PERSISTENCE_FILE, "r") as f:
                orders = json.load(f)
            print(f"✅ Loaded {len(orders)} orders from local persistence")
        except Exception as e:
            print(f"⚠️ Error loading local persistence: {e}")
            orders = []
    else:
        orders = []

def save_orders_locally():
    try:
        with open(PERSISTENCE_FILE, "w") as f:
            json.dump(orders, f, indent=2)
        print(f"✅ Saved {len(orders)} orders to local persistence")
    except Exception as e:
        print(f"⚠️ Error saving local persistence: {e}")

# Initial load
load_orders_locally()

# Settings persistence
settings = {
    "fb_pixel_id": "",
    "tiktok_pixel_id": ""
}
SETTINGS_FILE = "settings_persistence.json"

def load_settings_locally():
    global settings
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                settings.update(json.load(f))
            print(f"✅ Loaded settings from local persistence")
        except Exception as e:
            print(f"⚠️ Error loading settings persistence: {e}")

def save_settings_locally():
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=2)
        print(f"✅ Saved settings to local persistence")
    except Exception as e:
        print(f"⚠️ Error saving settings persistence: {e}")

# Initial load for settings
load_settings_locally()

# Agent persistence
agents_list = []
AGENTS_FILE = "agents_persistence.json"

def load_agents_locally():
    global agents_list
    try:
        if os.path.exists(AGENTS_FILE):
            with open(AGENTS_FILE, "r") as f:
                agents_list = json.load(f)
            print(f"✅ Loaded {len(agents_list)} agents from local persistence")
        else:
            agents_list = []
    except Exception as e:
        print(f"❌ Error loading agents locally: {e}")
        agents_list = []

def save_agents_locally():
    try:
        with open(AGENTS_FILE, "w") as f:
            json.dump(agents_list, f)
        print(f"✅ Saved {len(agents_list)} agents to local persistence")
    except Exception as e:
        print(f"❌ Error saving agents locally: {e}")

# Initial load for agents
load_agents_locally()

def is_supabase_reachable():
    """Check if Supabase domain is resolvable to avoid crashing on DNS errors"""
    if not SUPABASE_URL:
        return False
    try:
        domain = urlparse(SUPABASE_URL).netloc
        socket.gethostbyname(domain)
        return True
    except:
        return False

def get_supabase_headers():
    """Get headers for Supabase API calls"""
    return {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

# Helper for matching frames
def get_frame_by_id(frame_id):
    for f in FRAMES_DATA:
        if str(f["id"]) == str(frame_id):
            return f
    return FRAMES_DATA[0]

# Local Storage Helpers
def save_file_locally(file_data, filename, subfolder="audio"):
    """Save file to local uploads directory and return relative URL"""
    try:
        upload_dir = os.path.join("uploads", subfolder)
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir, exist_ok=True)
            
        file_path = os.path.join(upload_dir, filename)
        
        # If file_data is a Flask file object
        if hasattr(file_data, 'save'):
            file_data.seek(0)
            file_data.save(file_path)
        else:
            # If file_data is bytes
            with open(file_path, "wb") as f:
                f.write(file_data)
                
        print(f"✅ File saved locally: {file_path}")
        # Return relative URL that Next.js proxy/Nginx can handle
        return f"/api/uploads/{subfolder}/{filename}"
    except Exception as e:
        print(f"❌ Local save error: {e}")
        return None

@app.route('/api/uploads/<path:filename>')
def serve_uploads(filename):
    """Serve files from the uploads directory"""
    return send_from_directory('uploads', filename)

def upload_audio_to_cloudinary(audio_file):
    """Upload audio file to Cloudinary with local fallback"""
    filename = f"audio_{uuid.uuid4()}.webm"
    
    # Try Cloudinary first
    if CLOUDINARY_AVAILABLE:
        try:
            # Re-seek to 0 if it's a file object
            if hasattr(audio_file, 'seek'):
                audio_file.seek(0)
                
            result = cloudinary.uploader.upload(
                audio_file,
                resource_type="video",
                folder="audio_frame_art/audio",
                public_id=filename.split('.')[0],
                format="mp3"
            )
            print(f"✅ Audio uploaded to Cloudinary: {result['secure_url']}")
            return result["secure_url"]
        except Exception as e:
            print(f"❌ Cloudinary upload error: {e}")
    
    # Fallback to local storage
    print("⚠️  Falling back to local storage for audio...")
    return save_file_locally(audio_file, filename, "audio")

def upload_to_cloudinary(file_path, folder="audio_frame_art/waveforms", resource_type="image"):
    """Upload file to Cloudinary"""
    if not CLOUDINARY_AVAILABLE:
        print("⚠️  Cloudinary not available, cannot upload file")
        return None
    
    try:
        with open(file_path, 'rb') as f:
            result = cloudinary.uploader.upload(
                f,
                folder=folder,
                resource_type=resource_type
            )
            return result["secure_url"]
    except Exception as e:
        print(f"❌ Cloudinary upload error: {e}")
        return None

def check_and_create_bucket(supabase: Client, bucket_name: str = "wave_codes"):
    """Check if bucket exists, create if it doesn't exist"""
    try:
        # Try to list buckets to see if wave_codes exists
        buckets = supabase.storage.list_buckets()
        
        bucket_exists = False
        for bucket in buckets:
            if bucket.name == bucket_name:
                bucket_exists = True
                print(f"✅ Bucket '{bucket_name}' already exists")
                break
        
        if not bucket_exists:
            print(f"⚠️  Bucket '{bucket_name}' not found. Creating...")
            # Note: Creating buckets requires service role key, not anon key
            # For now, we'll just try to upload and see if it works
            print(f"   Please create the '{bucket_name}' bucket manually in Supabase Dashboard")
            print(f"   Dashboard: {SUPABASE_URL.replace('/rest/v1', '')}")
            return False
        
        return True
    except Exception as e:
        print(f"⚠️  Could not check bucket existence: {e}")
        print(f"   Attempting upload anyway...")
        return True  # Assume it exists and try upload

def upload_waveform_to_supabase_storage(image_bytes: bytes, filename: str) -> str:
    """Upload waveform code to Supabase Storage (wave_codes bucket)."""
    if not SUPABASE_STORAGE_AVAILABLE:
        print("❌ CRITICAL: Supabase Storage not available!")
        print("   Install with: pip install supabase")
        return None
    
    try:
        print(f"\n📤 UPLOADING WAVEFORM CODE TO SUPABASE STORAGE...")
        print(f"   Filename: {filename}")
        print(f"   Image size: {len(image_bytes)} bytes")
        
        # Initialize Supabase client
        supabase: Client = create_client(
            SUPABASE_URL,
            SUPABASE_ANON_KEY
        )
        
        print(f"✅ Supabase client initialized")
        print(f"   URL: {SUPABASE_URL}")
        
        # Ensure filename has .png extension
        if not filename.endswith('.png'):
            filename = f"{filename}.png"
        
        print(f"\n📦 Uploading to 'wave_codes' bucket...")
        print(f"   Bucket: wave_codes")
        print(f"   File: {filename}")
        
        # CRITICAL: Upload to wave_codes bucket
        # Supabase Storage upload accepts bytes directly
        # Upload using the correct Supabase Storage API
        result = supabase.storage.from_("wave_codes").upload(
            path=filename,
            file=image_bytes,  # Direct bytes
            file_options={
                "content-type": "image/png",
                "upsert": "true"
            }
        )
        
        print(f"   Upload response: {result}")
        print(f"   Response type: {type(result)}")
        
        # Check for errors - result can be dict, list, or None
        if result is None:
            raise Exception("❌ Upload returned None - bucket might not exist or permissions wrong!")
        
        # Check if result has error
        if isinstance(result, dict):
            if result.get('error') or result.get('errorCode'):
                error_msg = result.get('message', result.get('error', str(result)))
                raise Exception(f"❌ Supabase upload error: {error_msg}")
            elif result.get('path') or result.get('id'):
                # Success case - got path or id
                print(f"✅ Upload successful! Got path/id: {result.get('path') or result.get('id')}")
        
        # Get the public URL - THIS IS CRITICAL
        print(f"\n📎 Getting public URL...")
        try:
            # Try to get public URL
            public_url_response = supabase.storage.from_("wave_codes").get_public_url(filename)
            
            if isinstance(public_url_response, str):
                public_url = public_url_response
            elif isinstance(public_url_response, dict):
                public_url = public_url_response.get('publicUrl') or public_url_response.get('url') or str(public_url_response)
            else:
                # Construct URL manually if needed
                project_ref = SUPABASE_URL.split('//')[1].split('.')[0] if '//' in SUPABASE_URL else 'qksmfogjdurxgzmlcujb'
                public_url = f"https://{project_ref}.supabase.co/storage/v1/object/public/wave_codes/{filename}"
                print(f"   ⚠️  Constructed URL manually: {public_url}")
            
            print(f"\n✅✅✅ WAVEFORM CODE SUCCESSFULLY UPLOADED TO SUPABASE STORAGE!")
            print(f"   Public URL: {public_url}")
            print(f"   File: {filename}")
            print(f"   Size: {len(image_bytes)} bytes")
            
            # CRITICAL VERIFICATION: List files in bucket
            try:
                print(f"\n🔍 Verifying upload by listing files in bucket...")
                files_list = supabase.storage.from_("wave_codes").list()
                print(f"   Files list response: {files_list}")
                
                if isinstance(files_list, list):
                    file_names = [f.get('name') if isinstance(f, dict) else str(f) for f in files_list]
                    print(f"   Files in bucket ({len(file_names)}): {file_names[:5]}...")
                    if filename in file_names:
                        print(f"   ✅✅ VERIFIED: '{filename}' exists in bucket!")
                    else:
                        print(f"   ⚠️  File not in listing (may need refresh)")
                else:
                    print(f"   ⚠️  Could not parse files list: {type(files_list)}")
            except Exception as verify_error:
                print(f"   ⚠️  Verification listing failed: {verify_error}")
            
            return public_url
            
        except Exception as url_error:
            print(f"❌ Error getting public URL: {url_error}")
            # Still return constructed URL
            project_ref = SUPABASE_URL.split('//')[1].split('.')[0] if '//' in SUPABASE_URL else 'qksmfogjdurxgzmlcujb'
            constructed_url = f"https://{project_ref}.supabase.co/storage/v1/object/public/wave_codes/{filename}"
            print(f"   Using constructed URL: {constructed_url}")
            return constructed_url
        
    except Exception as e:
        print(f"\n❌❌❌ CRITICAL: Supabase Storage upload FAILED!")
        print(f"   Error: {e}")
        print(f"   Error type: {type(e).__name__}")
        
        # LOCAL FALLBACK for waveform image
        try:
            print(f"🔧 FALLING BACK TO LOCAL STORAGE FOR WAVEFORM...")
            local_path = save_file_locally(image_bytes, filename, subfolder="waveforms")
            if local_path:
                print(f"✅ Saved waveform locally: {local_path}")
                # Construct local URL
                local_url = f"/uploads/waveforms/{filename}"
                return local_url
        except Exception as local_err:
            print(f"❌ Local fallback failed: {local_err}")

        return None

def generate_spotify_waveform_code(audio_url, scan_id, frame_id=None):
    """Generate Spotify-style waveform code for audio URL and upload to Supabase Storage
    The waveform code can be scanned by mobile app to play the audio.
    Matches Spotify code style from: https://boonepeter.github.io/imgs/spotify/spotify_track_6vQN2a9QSgWcm74KEZYfDL.jpg
    """
    try:
        print(f"🎵 Generating Spotify waveform code for scan_id: {scan_id}")
        
        # Download or load audio data
        try:
            if audio_url.startswith('/api/uploads/'):
                # Handle local relative URL
                file_path = audio_url.replace('/api/uploads/', 'uploads/')
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        audio_data = f.read()
                    print(f"✅ Loaded local audio file: {len(audio_data)} bytes")
                else:
                    raise FileNotFoundError(f"Local audio file not found: {file_path}")
            else:
                # Handle external URL
                response = requests.get(audio_url, timeout=30)
                response.raise_for_status()
                audio_data = response.content
                print(f"✅ Downloaded audio file: {len(audio_data)} bytes")
        except Exception as e:
            print(f"❌ Failed to get audio for waveform: {e}")
            # Generate fallback waveform
            return generate_fallback_waveform(scan_id, frame_id)
        
        # Analyze audio waveform
        waveform_data = analyze_audio_waveform(audio_data)
        
        # Create QR code data URL for mobile app scanning (format: audio_frame://frame/{frame_id})
        if scan_id:
            qr_data_url = f"audio_frame://play/{scan_id}"
            print(f"📱 QR code data for scanning: {qr_data_url}")
        elif frame_id:
            qr_data_url = f"audio_frame://frame/{frame_id}"
            print(f"📱 QR code data for scanning: {qr_data_url}")
        
        # Create Spotify waveform image
        waveform_image = create_spotify_waveform_image(waveform_data, scan_id, qr_data_url)
        
        # Upload directly to Supabase Storage (primary method)
        waveform_filename = f"spotify_waveform_{scan_id}.png"
        print(f"🎨 Created waveform image: {len(waveform_image)} bytes")
        waveform_url = None
        
        if SUPABASE_STORAGE_AVAILABLE:
            waveform_url = upload_waveform_to_supabase_storage(waveform_image, waveform_filename)
        
        # If Supabase Storage failed, save locally
        if not waveform_url:
            print("⚠️  Supabase Storage failed or unavailable, saving waveform locally...")
            waveform_url = save_file_locally(waveform_image, waveform_filename, "waveforms")
        
        # Create waveform data for storage (includes audio URL for mobile app scanning)
        waveform_data_json = {
            "type": "spotify_waveform",
            "scan_id": scan_id,
            "audio_url": audio_url,  # Mobile app uses this to play audio when scanning
            "waveform_url": waveform_url,  # Supabase Storage URL of the waveform image
            "scannable": True,  # Indicates this can be scanned by mobile app
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "waveform_url": waveform_url,
            "waveform_data": json.dumps(waveform_data_json)
        }
        
    except Exception as e:
        print(f"❌ Spotify waveform generation error: {e}")
        return generate_fallback_waveform(scan_id)

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

def create_spotify_waveform_image(waveform_data, scan_id=None, qr_data_url=None):
    """Create the Spotify-style waveform code image with vertical bars
    Shows the waveform and the scan_id at the bottom.
    """
    width = 800
    height = 250
    bar_count = len(waveform_data)
    bar_width = 8
    bar_spacing = 4
    max_bar_height = 140
    
    # Create white background
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Calculate total width needed for bars
    total_bars_width = bar_count * (bar_width + bar_spacing) - bar_spacing
    start_x = (width - total_bars_width) // 2
    
    # Draw waveform bars
    # Center bars vertically in the top part
    bars_y_center = 100
    for i, amplitude in enumerate(waveform_data):
        bar_height = max(8, int(amplitude * max_bar_height))
        y_start = bars_y_center - (bar_height // 2)
        y_end = y_start + bar_height
        
        x_start = start_x + i * (bar_width + bar_spacing)
        x_end = x_start + bar_width
        
        corner_radius = min(bar_width // 2, max(2, (y_end - y_start) // 4))
        if corner_radius <= 0 or bar_height < 8:
            draw.rectangle([x_start, y_start, x_end, y_end], fill='black')
        else:
            draw.rounded_rectangle([x_start, y_start, x_end, y_end], 
                                  radius=corner_radius, fill='black')
    
    # Add Scan ID text at the bottom
    # User requested: wave plus id number in bottom nothing else
    if scan_id:
        try:
            # Try to load a font (installed in Dockerfile)
            font_size = 32
            font = None
            font_paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
            ]
            for path in font_paths:
                if os.path.exists(path):
                    font = ImageFont.truetype(path, font_size)
                    break
            
            if not font:
                font = ImageFont.load_default()
            
            text = f"#{scan_id}"
            
            # Center the text
            if hasattr(draw, 'textbbox'):
                bbox = draw.textbbox((0, 0), text, font=font)
                text_w = bbox[2] - bbox[0]
            else:
                text_w, _ = draw.textsize(text, font=font)
            
            text_x = (width - text_w) // 2
            text_y = height - 60  # Positioned at the bottom
            
            draw.text((text_x, text_y), text, fill='black', font=font)
            print(f"✅ Added Scan ID to waveform: {text}")
        except Exception as e:
            print(f"⚠️ Could not add text to waveform image: {e}")
            
    # Convert to bytes
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG', optimize=True)
    return img_byte_arr.getvalue()

def generate_fallback_waveform(scan_id, frame_id=None):
    """Generate a fallback waveform when audio analysis fails"""
    try:
        print(f"🎵 Generating fallback Spotify waveform for scan_id {scan_id}")
        
        # Generate realistic waveform pattern
        waveform_data = generate_realistic_waveform()
        
        # Create QR code data URL for mobile app scanning
        if scan_id:
            qr_data_url = f"audio_frame://play/{scan_id}"
            print(f"📱 QR code data for scanning: {qr_data_url}")
        elif frame_id:
            qr_data_url = f"audio_frame://frame/{frame_id}"
            print(f"📱 QR code data for scanning: {qr_data_url}")
        
        # Create Spotify waveform image
        waveform_image = create_spotify_waveform_image(waveform_data, scan_id, qr_data_url)
        
        # Upload directly to Supabase Storage (primary method)
        waveform_filename = f"spotify_fallback_{scan_id}.png"
        print(f"🎨 Created fallback waveform image: {len(waveform_image)} bytes")
        waveform_url = None
        
        if SUPABASE_STORAGE_AVAILABLE:
            waveform_url = upload_waveform_to_supabase_storage(waveform_image, waveform_filename)
        
        # If Supabase Storage failed, save locally
        if not waveform_url:
            print("⚠️  Supabase Storage failed or unavailable for fallback, saving locally...")
            waveform_url = save_file_locally(waveform_image, waveform_filename, "waveforms")
        
        # IMPORTANT: If Supabase Storage upload fails, we MUST retry or use fallback
        if not waveform_url:
            print("❌ CRITICAL: Supabase Storage upload failed for fallback waveform!")
            print("🔄 Attempting retry...")
            
            # Retry with timestamp-based filename
            import time
            timestamp = int(time.time())
            waveform_filename_retry = f"spotify_waveform_fallback_{order_id}_{timestamp}.png"
            waveform_url = upload_waveform_to_supabase_storage(waveform_image, waveform_filename_retry)
            
            if not waveform_url:
                print("❌ Retry also failed. Using local storage fallback...")
                waveform_dir = "uploads/waveforms"
                if not os.path.exists(waveform_dir):
                    os.makedirs(waveform_dir)
                
                waveform_path = os.path.join(waveform_dir, waveform_filename)
                with open(waveform_path, "wb") as f:
                    f.write(waveform_image)
                
                print(f"✅ Fallback waveform saved locally: {waveform_path}")
                
                # Try Cloudinary as backup
                cloudinary_waveform_url = upload_to_cloudinary(
                    waveform_path, 
                    folder="audio_frame_art/waveforms", 
                    resource_type="image"
                )
                
                if cloudinary_waveform_url:
                    waveform_url = cloudinary_waveform_url
                    print(f"   ⚠️  NOTE: Using Cloudinary instead of Supabase Storage")
                else:
                    waveform_url = f"http://localhost:8001/uploads/waveforms/{waveform_filename}"
                    print(f"   ⚠️  CRITICAL: Waveform NOT in Supabase Storage!")
        
        # Create waveform data for storage (fallback waveform - no audio URL available)
        waveform_data_json = {
            "type": "spotify_waveform",
            "order_id": order_id,
            "waveform_url": waveform_url,  # Supabase Storage URL of the waveform image
            "fallback": True,  # Indicates this is a fallback (no audio available)
            "scannable": False,  # Cannot play audio since no audio URL
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
    """Save order to Supabase database - MUST SUCCEED"""
    try:
        print(f"\n{'='*60}")
        print(f"💾 ATTEMPTING TO SAVE ORDER TO SUPABASE")
        print(f"{'='*60}")
        print(f"   Customer: {order_data.get('customer_name', 'N/A')}")
        print(f"   Phone: {order_data.get('customer_phone', 'N/A')}")
        print(f"   Frame: {order_data.get('frame_title', 'N/A')}")
        print(f"   Amount: {order_data.get('total_amount', 'N/A')}")
        
        # Validate Supabase configuration
        if not SUPABASE_URL or SUPABASE_URL == "":
            print(f"❌ CRITICAL: SUPABASE_URL is not configured!")
            return None
        
        if not SUPABASE_ANON_KEY or SUPABASE_ANON_KEY == "":
            print(f"❌ CRITICAL: SUPABASE_ANON_KEY is not configured!")
            return None
        
        # Try to save to the api_order table
        url = f"{SUPABASE_URL}/rest/v1/api_order"
        headers = get_supabase_headers()
        
        print(f"   Supabase URL: {SUPABASE_URL}")
        print(f"   API Endpoint: {url}")
        print(f"   Has API Key: {bool(SUPABASE_ANON_KEY)}")
        
        # Map our data to the existing table structure (include audio and WAVEFORM CODE columns)
        supabase_data = {
            "customer_name": order_data.get("customer_name", ""),
            "customer_phone": order_data.get("customer_phone", ""),
            "customer_email": order_data.get("customer_email", ""),
            "delivery_address": order_data.get("delivery_address", ""),
            "city": order_data.get("city", ""),
            "wilaya": order_data.get("wilaya", ""),  # Add wilaya if table supports it
            "baladya": order_data.get("baladya", ""),  # Add baladya if table supports it
            "postal_code": order_data.get("postal_code", "00000"),  # Default value for NOT NULL constraint
            "frame_id": order_data.get("frame_id", 1),
            "audio_file_url": order_data.get("audio_file_url", ""),
            "qr_code_url": order_data.get("qr_code_url", ""),  # WAVEFORM CODE URL from Supabase Storage
            "qr_code_data": order_data.get("qr_code_data", ""),  # WAVEFORM METADATA with audio_url
            "status": order_data.get("status", "pending"),
            "payment_method": order_data.get("payment_method", "COD"),
            "total_amount": float(order_data.get("total_amount", 0)),  # Ensure it's a number
            "notes": order_data.get("notes", ""),
            "scan_id": order_data.get("scan_id", "")
        }
        
        # Remove empty wilaya/baladya if table doesn't support them (will be handled by try/except)
        if not supabase_data.get("wilaya"):
            supabase_data.pop("wilaya", None)
        if not supabase_data.get("baladya"):
            supabase_data.pop("baladya", None)
        
        # CRITICAL: Log what we're saving
        print(f"\n💾 SAVING WAVEFORM CODE TO DATABASE:")
        print(f"   audio_file_url: {supabase_data.get('audio_file_url', 'EMPTY')[:50]}...")
        print(f"   qr_code_url (waveform): {supabase_data.get('qr_code_url', 'EMPTY')[:80]}...")
        print(f"   qr_code_data has data: {bool(supabase_data.get('qr_code_data'))}")
        if supabase_data.get('qr_code_data'):
            try:
                # Use global json module instead of local import
                metadata = json.loads(supabase_data['qr_code_data'])
                print(f"   Metadata type: {metadata.get('type')}")
                print(f"   Has audio_url: {'audio_url' in metadata}")
            except Exception as e:
                print(f"   ⚠️ Could not parse metadata: {e}")
        
        print(f"   Sending data to: {url}")
        # Only log first 50 chars of data fields to avoid huge logs
        log_data = supabase_data.copy()
        if log_data.get('qr_code_data'):
            log_data['qr_code_data'] = log_data['qr_code_data'][:50] + "..."
        if log_data.get('audio_file_url'):
            log_data['audio_file_url'] = log_data['audio_file_url'][:50] + "..."
            
        print(f"   Data summary: {json.dumps(log_data, indent=2)}")
        
        response = requests.post(url, headers=headers, json=supabase_data)
        
        print(f"   Response status: {response.status_code}")
        print(f"   Response text: {response.text}")
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"✅ Order saved to Supabase successfully!")
            print(f"   Order ID: {result[0]['id'] if isinstance(result, list) else result.get('id', 'N/A')}")
            print(f"   Supabase response: {result}")
            return result if isinstance(result, list) else [result] if result else None
        else:
            print(f"❌ Supabase error: {response.status_code} - {response.text}")
            print(f"❌ FAILED to save order to Supabase database!")
            print(f"   URL: {url}")
            print(f"   Headers: {headers}")
            print(f"   This is a CRITICAL error - order will NOT be saved!")
            return None
    except Exception as e:
        print(f"❌ Error saving to Supabase: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_orders_from_supabase(search=None, status=None):
    """Get orders from Supabase database with filtering"""
    try:
        print(f"📥 Fetching orders from Supabase (search={search}, status={status})...")
        url = f"{SUPABASE_URL}/rest/v1/api_order"
        
        params = {
            "select": "*",
            "order": "created_at.desc"
        }
        
        if status:
            params["status"] = f"eq.{status}"
            
        if search:
            # Supabase or-logic: (col1.ilike.*search*,col2.ilike.*search*)
            params["or"] = f"(customer_name.ilike.*{search}*,customer_phone.ilike.*{search}*,scan_id.ilike.*{search}*)"
            
        headers = get_supabase_headers()
        
        response = requests.get(url, headers=headers, params=params)
        
        print(f"   Response status: {response.status_code}")
        
        if response.status_code == 200:
            orders_list = response.json()
            print(f"✅ Retrieved {len(orders_list)} orders from Supabase")
            return orders_list
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
    print(f"DEBUG: handle_orders called with method {request.method}")
    if request.method == 'GET':
        # Get pagination and filter parameters
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 30))
        search = request.args.get('search')
        status_filter = request.args.get('status')
        offset = (page - 1) * limit
        
        # Get filtered orders from Supabase
        supabase_orders = get_orders_from_supabase(search=search, status=status_filter)
        
        # Merge with local orders (apply same filtering locally)
        global orders
        all_orders = []
        
        # Local filtering
        for o in orders:
            matches_status = not status_filter or o.get('status') == status_filter
            matches_search = not search or any(
                search.lower() in str(o.get(field, '')).lower() 
                for field in ['customer_name', 'customer_phone', 'scan_id']
            )
            if matches_status and matches_search:
                all_orders.append(o)
        
        # Add supabase orders that aren't already in local orders (by ID)
        existing_ids = {o.get('id') for o in all_orders}
        for so in supabase_orders:
            if so.get('id') not in existing_ids:
                all_orders.append(so)
        
        # Sort by creation date (newest first)
        all_orders.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        total = len(all_orders)
        
        start = offset
        end = offset + limit
        paginated_orders = all_orders[start:end]
        return jsonify({
            "orders": paginated_orders,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": (total + limit - 1) // limit
        })
    
    elif request.method == 'POST':
        try:
            print(f"\n🆕 New order request received")
            
            # Get data from request
            if request.is_json:
                data = request.get_json()
                audio_file = None
            else:
                data = request.form.to_dict()
                audio_file = request.files.get('audio_file')
            
            print(f"   Data received: {data}")
            
            # Validate required fields
            if not data:
                return jsonify({"error": "No data received"}), 400
            
            # Check for required fields with variations
            customer_name = data.get("customer_name", "").strip()
            first_name = data.get("first_name", "").strip()
            last_name = data.get("last_name", "").strip()
            
            # If customer_name is not provided, construct from first_name + last_name
            if not customer_name:
                if first_name and last_name:
                    customer_name = f"{first_name} {last_name}".strip()
                elif first_name:
                    customer_name = first_name
                elif last_name:
                    customer_name = last_name
            
            phone = (data.get("customer_phone") or data.get("phone", "")).strip()
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
            
            # Find frame
            frame = get_frame_by_id(frame_id)
            if not frame:
                return jsonify({"error": "Frame not found"}), 400
            
            # Handle audio file upload
            audio_url = None
            waveform_data = None
            audio_file = None
            
            if 'audio_file' in request.files:
                audio_file = request.files['audio_file']
            
            if audio_file and hasattr(audio_file, 'filename') and audio_file.filename:
                    print(f"📁 Uploading audio file: {audio_file.filename}")
                    # Upload audio to Cloudinary
                    audio_url = upload_audio_to_cloudinary(audio_file)
                    if audio_url:
                        print(f"✅ Audio uploaded to Cloudinary: {audio_url}")
                    else:
                        print(f"❌ Failed to upload audio to Cloudinary")
                        # Still try to proceed, audio_url will be None
            
            # Extract additional fields
            wilaya = data.get("wilaya", "")
            baladya = data.get("baladya", "") or data.get("baladiya", "")
            
            # Generate unique scan_id (15 chars hex like reference image)
            scan_id = uuid.uuid4().hex[:15].upper()
            order_id = uuid.uuid4().int % 1000000  # Internal numeric ID
            
            # Generate Spotify waveform code if audio was uploaded
            # Generate Spotify waveform code (always distinct from QR)
            print(f"\n🎵 Generating Spotify waveform code for scan_id: {scan_id}")
            waveform_data = None
            
            if audio_url:
                print(f"   Audio URL: {audio_url}")
                waveform_result = generate_spotify_waveform_code(audio_url, scan_id, frame_id)
                if waveform_result and waveform_result.get('waveform_url'):
                    waveform_data = waveform_result
                    print(f"✅ Spotify waveform code generated successfully!")
                else:
                     print(f"❌ Failed to generate from audioUrl, trying fallback...")
            
            # If no waveform data yet (no audio or failed), generate fallback
            if not waveform_data:
                print(f"⚠️  Using fallback waveform generation (no audio or failed)...")
                waveform_result = generate_fallback_waveform(scan_id, frame_id)
                if waveform_result and waveform_result.get('waveform_url'):
                    waveform_data = waveform_result
                    print(f"✅ Fallback waveform generated successfully!")
            
            # Prepare order data - IMPORTANT: Use qr_code_url and qr_code_data columns for waveform codes
            order_data = {
                "customer_name": customer_name.strip(),
                "customer_phone": phone,
                "customer_email": data.get("customer_email", ""),
                "delivery_address": address,
                "city": city,
                "postal_code": data.get("postal_code", "00000"),
                "wilaya": wilaya,
                "baladya": baladya,
                "frame_id": frame_id,
                "frame_title": frame["title"],
                "frame_type": frame["frame_type"],
                "audio_file_url": audio_url or "",
                "qr_code_url": waveform_data["waveform_url"] if waveform_data else "",  # WAVEFORM CODE URL (stored in qr_code_url column)
                "qr_code_data": waveform_data["waveform_data"] if waveform_data else "",  # WAVEFORM METADATA (stored in qr_code_data column)
                "status": "pending",
                "payment_method": "COD",
                "total_amount": 4000.0, # Fixed total: 3500 Product + 500 Delivery
                "notes": data.get("notes", ""),
                "scan_id": scan_id,
                "created_at": datetime.now().isoformat()
            }
            
            # Print confirmation
            if waveform_data:
                print(f"\n✅ WAVEFORM CODE DATA READY:")
                print(f"   Waveform URL: {order_data['qr_code_url']}")
                print(f"   Contains audio URL: {'audio_url' in order_data['qr_code_data']}")
            
            # Save to Supabase - MUST SUCCEED, NO FALLBACK
            print(f"💾 Saving order to Supabase...")
            supabase_result = save_order_to_supabase(order_data)
            
            if not supabase_result:
                print(f"⚠️  LOCAL FALLBACK: Could not save to Supabase, keeping in local memory only.")
                order_data['id'] = order_id
                order_data['supabase_error'] = True
                orders.append(order_data)
                save_orders_locally()
                
                return jsonify({
                    "success": True,
                    "message": "Order created locally (cloud off)",
                    "id": order_id,
                    "order_id": order_id,
                    "scan_id": scan_id,
                    "audio_url": order_data.get("audio_file_url"),
                    "waveform_url": order_data.get("qr_code_url"),
                    "order": order_data
                }), 201
            
            # If Supabase succeeded, use its ID
            final_order_id = supabase_result[0]['id'] if isinstance(supabase_result, list) else supabase_result.get('id', order_id)
            order_data['id'] = final_order_id
            
            # Also keep a local copy for scanning backup
            orders.append(order_data)
            save_orders_locally()

            print(f"✅ Order saved to Supabase successfully!")
            print(f"✅ Order ID: {final_order_id}")
            
            return jsonify({
                "success": True,
                "message": "Order created successfully",
                "id": final_order_id,
                "order_id": final_order_id,
                "scan_id": scan_id,
                "audio_url": order_data.get("audio_file_url"),
                "waveform_url": order_data.get("qr_code_url"),
                "order": order_data
            }), 201
            
        except Exception as e:
            print(f"❌ Error creating order: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

@app.route('/api/orders/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update order status and confirmation agent"""
    try:
        data = request.get_json()
        status = data.get('status')
        confirmation_agent = data.get('confirmation_agent')
        
        print(f"🔄 Updating order {order_id} status to {status}, agent: {confirmation_agent}")
        
        if not status:
            return jsonify({"error": "Status is required"}), 400
            
        # Update in Supabase
        # Prepare payload
        payload = {"status": status}
        if confirmation_agent is not None:
            payload["confirmation_agent"] = confirmation_agent
            
        # Call Supabase API
        url = f"{SUPABASE_URL}/rest/v1/api_order?id=eq.{order_id}"
        headers = get_supabase_headers()
        
        response = requests.patch(url, headers=headers, json=payload)
        
        if response.status_code in [200, 204]:
            print(f"✅ Order {order_id} updated successfully")
            return jsonify({"success": True, "message": "Order updated successfully"})
        else:
            print(f"❌ Failed to update order {order_id}: {response.text}")
            return jsonify({"error": "Failed to update order", "details": response.text}), 500
            
    except Exception as e:
        print(f"❌ Error updating order: {e}")
        # Local fallback
        try:
            global orders
            print(f"🔧 FALLBACK: Updating local order {order_id} status...")
            
            updated = False
            for o in orders:
                if str(o.get('id')) == str(order_id):
                    o['status'] = status
                    if confirmation_agent is not None:
                        o['confirmation_agent'] = confirmation_agent
                    updated = True
                    break
            
            if updated:
                save_orders_locally()
                print(f"✅ FALLBACK SUCCESS: Order updated locally")
                return jsonify({"success": True, "message": "Order updated locally (cloud unavailable)"})
            else:
                return jsonify({"error": "Order not found locally"}), 404
        except Exception as local_err:
             print(f"❌ Local fallback failed: {local_err}")
             return jsonify({"error": str(e)}), 500

@app.route('/api/orders/<order_id>', methods=['PUT', 'DELETE'])
def update_or_delete_order(order_id):
    """Update or delete order in Supabase"""
    try:
        if request.method == 'PUT':
            updates = request.get_json()
            print(f"🔄 Updating order {order_id} details: {updates}")
            
            url = f"{SUPABASE_URL}/rest/v1/api_order?id=eq.{order_id}"
            headers = get_supabase_headers()
            
            response = requests.patch(url, headers=headers, json=updates)
            
            if response.status_code in [200, 204]:
                print(f"✅ Order {order_id} updated successfully")
                return jsonify({"success": True, "message": "Order updated successfully"})
            else:
                print(f"❌ Failed to update order {order_id}: {response.text}")
                return jsonify({"error": "Failed to update order", "details": response.text}), 500
                
        elif request.method == 'DELETE':
            print(f"🗑️ Deleting order {order_id}")
            
            url = f"{SUPABASE_URL}/rest/v1/api_order?id=eq.{order_id}"
            headers = get_supabase_headers()
            
            response = requests.delete(url, headers=headers)
            
            if response.status_code in [200, 204]:
                print(f"✅ Order {order_id} deleted successfully")
                return jsonify({"success": True, "message": "Order deleted successfully"})
            else:
                print(f"❌ Failed to delete order {order_id}: {response.text}")
                return jsonify({"error": "Failed to delete order", "details": response.text}), 500
                
    except Exception as e:
        print(f"❌ Error processing request for order {order_id}: {e}")
        # Local fallback for both updates and deletes
        try:
            global orders
            print(f"🔧 FALLBACK START: Handling {request.method} for {order_id}. Orders count: {len(orders)}")
            
            order_id_int = int(order_id)
            updated = False
            
            if request.method == 'PUT':
                updates = request.get_json(silent=True) or {}
                print(f"🔧 FALLBACK: Updating local order {order_id} with {updates}...")
                
                for o in orders:
                    # IDs can be strings or ints in weak typing scenarios
                    if str(o.get('id')) == str(order_id):
                        o.update(updates)
                        updated = True
                        break
                
                if updated:
                    save_orders_locally()
                    print(f"✅ FALLBACK SUCCESS: Order updated locally")
                    return jsonify({"success": True, "message": "Order updated locally (cloud unavailable)"})
                else:
                    print(f"⚠️ FALLBACK: Order {order_id} not found in {len(orders)} local orders")
                    return jsonify({"error": "Order not found locally"}), 404
                    
            elif request.method == 'DELETE':
                print(f"🔧 FALLBACK: Deleting local order {order_id}...")
                initial_len = len(orders)
                # Filter out the deleted order
                new_list = [o for o in orders if str(o.get('id')) != str(order_id)]
                
                if len(new_list) < initial_len:
                    orders.clear()
                    orders.extend(new_list)
                    save_orders_locally()
                    print(f"✅ FALLBACK SUCCESS: Order deleted locally")
                    return jsonify({"success": True, "message": "Order deleted locally (cloud unavailable)"})
                else:
                     return jsonify({"error": "Order not found locally"}), 404
        except Exception as local_err:
             print(f"❌ Local fallback failed: {local_err}")
             import traceback
             traceback.print_exc()
             return jsonify({"error": str(e)}), 500

@app.route('/api/confirmation-agents/', methods=['GET', 'POST'])
def handle_confirmation_agents():
    """Manage confirmation agents"""
    global agents_list
    try:
        if request.method == 'GET':
            try:
                url = f"{SUPABASE_URL}/rest/v1/confirmation_agents?select=name"
                headers = get_supabase_headers()
                response = requests.get(url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    # Extract names from list of objects
                    cloud_agents = [a['name'] for a in response.json()]
                    # Merge with local agents (unique)
                    merged = list(set(cloud_agents + agents_list))
                    return jsonify(merged)
                else:
                    print(f"⚠️ Failed to fetch agents from cloud: {response.status_code}")
                    return jsonify(agents_list)
            except Exception as e:
                print(f"⚠️ Cloud agents unreachable: {e}")
                return jsonify(agents_list)
            
        elif request.method == 'POST':
            data = request.get_json()
            name = data.get('name')
            if not name:
                return jsonify({"error": "Name is required"}), 400
            
            # Save locally first
            if name not in agents_list:
                agents_list.append(name)
                save_agents_locally()
                
            try:
                url = f"{SUPABASE_URL}/rest/v1/confirmation_agents"
                headers = get_supabase_headers()
                # Check if agent already exists or handle unique constraint error
                response = requests.post(url, headers=headers, json={"name": name}, timeout=5)
                
                if response.status_code in [200, 201]:
                    return jsonify({"success": True, "name": name})
                elif response.status_code == 409: # Conflict
                    return jsonify({"success": True, "name": name, "message": "Agent already exists"})
                else:
                    print(f"⚠️ Failed to add agent to cloud: {response.status_code}")
                    return jsonify({"success": True, "name": name, "note": "Saved locally only"})
            except Exception as e:
                print(f"⚠️ Cloud agents unreachable for POST: {e}")
                return jsonify({"success": True, "name": name, "note": "Saved locally only"})
                
    except Exception as e:
        print(f"❌ Error managing agents: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/settings/', methods=['GET', 'POST'])
def handle_settings():
    """Handle settings - GET for retrieval, POST for update"""
    global settings
    try:
    try:
        if request.method == 'GET':
            # Sanitize before returning
            fb_id = settings.get("fb_pixel_id")
            if fb_id is None or str(fb_id).lower() == "null":
                fb_id = ""
                
            tt_id = settings.get("tiktok_pixel_id")
            if tt_id is None or str(tt_id).lower() == "null":
                tt_id = ""
                
            return jsonify({
                "fb_pixel_id": fb_id,
                "tiktok_pixel_id": tt_id
            })
        elif request.method == 'POST':
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data received"}), 400
            
            # Basic validation and trimming
            settings["fb_pixel_id"] = data.get("fb_pixel_id", settings["fb_pixel_id"])
            if settings["fb_pixel_id"]:
                settings["fb_pixel_id"] = str(settings["fb_pixel_id"]).strip()

            settings["tiktok_pixel_id"] = data.get("tiktok_pixel_id", settings["tiktok_pixel_id"])
            if settings["tiktok_pixel_id"]:
                settings["tiktok_pixel_id"] = str(settings["tiktok_pixel_id"]).strip()
            
            save_settings_locally()
            return jsonify({"success": True, "settings": settings})
    except Exception as e:
        print(f"❌ Error managing settings: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/confirmation-agents/<name>', methods=['DELETE'])
def delete_confirmation_agent(name):
    """Delete a confirmation agent"""
    try:
        print(f"🗑️ Deleting agent {name}")
        url = f"{SUPABASE_URL}/rest/v1/confirmation_agents?name=eq.{name}"
        headers = get_supabase_headers()
        
        response = requests.delete(url, headers=headers)
        
        if response.status_code in [200, 204]:
            return jsonify({"success": True})
        else:
            return jsonify({"error": "Failed to delete agent", "details": response.text}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/scan/<int:frame_id>/', methods=['GET'])
def scan_frame(frame_id):
    """Handle Spotify waveform code scan - returns audio from Supabase"""
    try:
        print(f"\n📱 ===== SCAN REQUEST ======")
        print(f"📱 Frame ID: {frame_id}")
        
        frame = next((f for f in FRAMES_DATA if f["id"] == frame_id), None)
        if not frame:
            print(f"❌ Frame {frame_id} not found")
            return jsonify({"error": "Frame not found"}), 404
        
        print(f"✅ Frame found: {frame['title']}")
        
        # Get orders from Supabase to find audio for this frame
        print(f"📥 Fetching orders from Supabase...")
        supabase_orders = get_orders_from_supabase()
        print(f"📥 Retrieved {len(supabase_orders)} orders from Supabase")
        
        audio_url = None
        waveform_url = None
        waveform_data = None
        order_found = None
        
        # Find the most recent order for this frame with audio
        print(f"🔍 Searching for orders with frame_id={frame_id} and audio...")
        matching_orders = []
        for order in supabase_orders:
            if order.get('frame_id') == frame_id:
                matching_orders.append(order)
                print(f"   Found order {order.get('id')} with frame_id={frame_id}")
                if order.get('audio_file_url'):
                    print(f"   ✅ Order {order.get('id')} has audio: {order.get('audio_file_url')[:60]}...")
        
        # Sort by created_at and get most recent with audio
        for order in sorted(supabase_orders, key=lambda x: x.get('created_at', ''), reverse=True):
            if order.get('frame_id') == frame_id and order.get('audio_file_url'):
                audio_url = order.get('audio_file_url')
                waveform_url = order.get('qr_code_url', '') or order.get('waveform_url', '')
                waveform_data = order.get('qr_code_data', '') or order.get('waveform_data', '')
                order_found = order
                print(f"✅ Selected order {order.get('id')} with audio")
                print(f"   Audio URL: {audio_url[:80]}...")
                break
        
        if not audio_url:
            print(f"❌ No audio found for frame_id={frame_id}")
            print(f"   Matching orders found: {len(matching_orders)}")
            for o in matching_orders:
                print(f"     Order {o.get('id')}: audio_file_url={bool(o.get('audio_file_url'))}")
            
            return jsonify({
                "frame_id": frame_id,
                "frame_title": frame["title"],
                "audio_url": "",
                "signed_audio_url": "",
                "message": "No audio file found for this frame. Please create an order with audio recording.",
                "error": "No audio available"
            }), 404
        
        response_data = {
        "frame_id": frame_id,
        "frame_title": frame["title"],
        "audio_url": audio_url,
            "signed_audio_url": audio_url,  # Ensure signed_audio_url is set
            "waveform_url": waveform_url,
        "message": "Audio file found successfully"
        }
        
        # Include waveform metadata for mobile app
        if waveform_data:
            try:
                waveform_metadata = json.loads(waveform_data)
                response_data["waveform_metadata"] = waveform_metadata
                # Use audio_url from metadata if available
                if waveform_metadata.get("audio_url"):
                    response_data["audio_url"] = waveform_metadata["audio_url"]
                    response_data["signed_audio_url"] = waveform_metadata["audio_url"]
                response_data["scannable"] = waveform_metadata.get("scannable", True)
            except Exception as e:
                print(f"⚠️  Could not parse waveform metadata: {e}")
                response_data["scannable"] = True
        
        print(f"✅ Returning scan response:")
        print(f"   frame_id: {response_data['frame_id']}")
        print(f"   frame_title: {response_data['frame_title']}")
        print(f"   audio_url: {response_data['audio_url'][:80]}...")
        print(f"   signed_audio_url: {response_data['signed_audio_url'][:80]}...")
        print(f"   ==========================")
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ Error in scan_frame: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "frame_id": frame_id,
            "message": "Error scanning frame"
        }), 500

@app.route('/api/play/<audio_id>/', methods=['GET'])
def play_audio(audio_id):
    """Get audio file URL by audio ID or order ID
    Supports multiple formats:
    - /api/play/<order_id>/ - Get audio by order ID
    - /api/play/<frame_id>/ - Get audio by frame ID (legacy)
    """
    try:
        print(f"\n🎵 ===== PLAY AUDIO REQUEST ======")
        print(f"🎵 Audio/Order ID: {audio_id}")
        
        # Try to parse as integer
        try:
            id_value = int(audio_id)
        except ValueError:
            return jsonify({
                "error": "Invalid audio ID format",
                "message": "Audio ID must be a number"
            }), 400
        
        # Get orders from Supabase
        supabase_orders = get_orders_from_supabase()
        
        # Try to find by order ID first, then by frame_id
        audio_url = None
        waveform_url = None
        order_info = None
        
        # Search by order ID (most direct)
        for order in supabase_orders:
            if order.get('id') == id_value and order.get('audio_file_url'):
                audio_url = order.get('audio_file_url')
                waveform_url = order.get('qr_code_url', '') or order.get('waveform_url', '')
                order_info = order
                print(f"✅ Found order by ID {id_value}")
                break
        
        # If not found by order ID, try by frame_id
        if not audio_url:
            for order in sorted(supabase_orders, key=lambda x: x.get('created_at', ''), reverse=True):
                if order.get('frame_id') == id_value and order.get('audio_file_url'):
                    audio_url = order.get('audio_file_url')
                    waveform_url = order.get('qr_code_url', '') or order.get('waveform_url', '')
                    order_info = order
                    print(f"✅ Found order by frame_id {id_value}")
                    break
        
        if not audio_url:
            print(f"❌ No audio found for ID {id_value}")
            return jsonify({
                "error": "Audio not found",
                "message": f"No audio file found for ID: {audio_id}",
                "audio_id": audio_id
            }), 404
        
        response_data = {
            "success": True,
            "audio_id": id_value,
            "audio_url": audio_url,
            "signed_audio_url": audio_url,  # Cloudinary URLs are already signed
            "waveform_url": waveform_url,
            "frame_title": order_info.get('frame_title', 'Unknown Frame') if order_info else 'Unknown Frame',
            "frame_id": order_info.get('frame_id') if order_info else None,
            "order_id": order_info.get('id') if order_info else None,
            "message": "Audio file found successfully"
        }
        
        print(f"✅ Returning audio URL: {audio_url[:80]}...")
        print(f"🎵 =================================")
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ Error in play_audio: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "audio_id": audio_id,
            "message": "Error retrieving audio"
        }), 500

@app.route('/api/test-qr/<int:frame_id>/', methods=['GET'])
def test_qr_code(frame_id):
    """Generate a test QR code image for frame_id - for testing scanner"""
    try:
        import qrcode
        from io import BytesIO
        import base64
        
        # Create QR code data
        qr_data = f"audio_frame://frame/{frame_id}"
        
        # Generate QR code - make it LARGE and easy to scan
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,  # Large boxes for easy scanning
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Create QR code image
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 for web display
        img_buffer = BytesIO()
        qr_img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        return jsonify({
            "success": True,
            "frame_id": frame_id,
            "qr_data": qr_data,
            "qr_image": f"data:image/png;base64,{img_base64}",
            "message": f"Test QR code for frame {frame_id}. Scan this to test!"
        })
    except Exception as e:
        print(f"❌ Error generating test QR: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/track-play/<int:frame_id>/', methods=['POST'])
def track_play(frame_id):
    """Track audio play event"""
    return jsonify({
        "message": "Play tracked successfully",
        "plays_count": 1
    })

# Simple in-memory cache for statistics
stats_cache = {
    "data": None,
    "timestamp": None
}

@app.route('/api/statistics/', methods=['GET'])
def get_statistics():
    """Get system statistics with simple 5-minute cache"""
    global stats_cache
    
    # Check cache (300 seconds = 5 minutes)
    if stats_cache["data"] and stats_cache["timestamp"]:
        if (datetime.now() - stats_cache["timestamp"]).total_seconds() < 300:
            return jsonify(stats_cache["data"])
            
    supabase_orders = get_orders_from_supabase()
    local_orders = orders
    
    total_orders = len(supabase_orders) + len(local_orders)
    
    stats_data = {
        "total_orders": total_orders,
        "supabase_orders": len(supabase_orders),
        "local_orders": len(local_orders),
        "total_frames": len(FRAMES_DATA),
        "total_scans": 0,
        "total_plays": 0,
        "pending_orders": len([o for o in supabase_orders if o.get("status") == "pending"]) + len([o for o in local_orders if o.get("status") == "pending"]),
        "delivered_orders": len([o for o in supabase_orders if o.get("status") == "delivered"]) + len([o for o in local_orders if o.get("status") == "delivered"])
    }
    
    # Update cache
    stats_cache["data"] = stats_data
    stats_cache["timestamp"] = datetime.now()
    
    return jsonify(stats_data)

@app.route('/api/health/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    # Test Supabase connection
    supabase_connected = False
    try:
        response = requests.get(f"{SUPABASE_URL}/rest/v1/api_order", headers=get_supabase_headers())
        supabase_connected = response.status_code == 200
    except:
        pass
    
    # Test Supabase Storage
    storage_status = {
        "available": SUPABASE_STORAGE_AVAILABLE,
        "bucket_exists": False,
        "bucket_accessible": False,
        "error": None
    }
    
    if SUPABASE_STORAGE_AVAILABLE:
        try:
            supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
            buckets = supabase.storage.list_buckets()
            
            # Check if wave_codes bucket exists
            for bucket in buckets:
                if bucket.name == "wave_codes":
                    storage_status["bucket_exists"] = True
                    # Try to list files in bucket to check accessibility
                    try:
                        files = supabase.storage.from_("wave_codes").list()
                        storage_status["bucket_accessible"] = True
                        storage_status["file_count"] = len(files) if isinstance(files, list) else 0
                    except Exception as e:
                        storage_status["error"] = str(e)
                    break
        except Exception as e:
            storage_status["error"] = str(e)
    
    return jsonify({
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "supabase_connected": supabase_connected,
        "supabase_url": SUPABASE_URL,
        "supabase_storage": storage_status,
        "total_orders": len(orders)
    })

@app.route('/api/test-storage/', methods=['GET'])
def test_storage():
    """Test endpoint to verify Supabase Storage is working"""
    if not SUPABASE_STORAGE_AVAILABLE:
        return jsonify({
            "error": "Supabase Storage not available",
            "message": "Install with: pip install supabase"
        }), 500
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        
        # Check buckets
        buckets = supabase.storage.list_buckets()
        bucket_names = [b.name for b in buckets]
        
        # Check if wave_codes exists
        wave_codes_exists = "wave_codes" in bucket_names
        
        result = {
            "supabase_url": SUPABASE_URL,
            "buckets_found": bucket_names,
            "wave_codes_exists": wave_codes_exists,
            "test_upload": None,
            "error": None
        }
        
        if wave_codes_exists:
            # Try to upload a test file
            try:
                test_data = b"test"
                test_result = supabase.storage.from_("wave_codes").upload(
                    "test_file.txt",
                    test_data,
                    file_options={"content-type": "text/plain", "upsert": "true"}
                )
                
                if test_result and not (isinstance(test_result, dict) and test_result.get('error')):
                    result["test_upload"] = "success"
                    # Try to get the file back
                    try:
                        files = supabase.storage.from_("wave_codes").list()
                        result["files_in_bucket"] = [f.get('name') for f in files] if isinstance(files, list) else []
                    except:
                        pass
                else:
                    result["test_upload"] = "failed"
                    result["error"] = str(test_result) if test_result else "Unknown error"
            except Exception as e:
                result["test_upload"] = "failed"
                result["error"] = str(e)
        else:
            result["error"] = "wave_codes bucket does not exist. Create it in Supabase Dashboard."
            result["instructions"] = [
                "1. Go to Supabase Dashboard → Storage",
                "2. Click 'Create a new bucket'",
                "3. Name: 'wave_codes'",
                "4. Set to PUBLIC",
                "5. Click 'Create bucket'"
            ]
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "error": str(e),
            "type": type(e).__name__
        }), 500

@app.route('/api/audio/<scan_id>/', methods=['GET'])
def audio_lookup(scan_id):
    """Direct lookup of an order by scan_id (the code printed on the waveform)"""
    try:
        print(f"\n🔍 ===== SCAN ID LOOKUP: {scan_id} =====")
        
        # 1. Try Supabase first (defensively)
        supabase_order = None
        if is_supabase_reachable():
            try:
                if SUPABASE_URL and SUPABASE_ANON_KEY:
                    print(f"📡 Supabase is reachable, checking cloud...")
                    supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
                    response = supabase.table('api_order').select('*').eq('scan_id', scan_id).execute()
                    
                    if not response.data and scan_id.isdigit():
                        response = supabase.table('api_order').select('*').eq('id', int(scan_id)).execute()
                    
                    if response.data:
                        supabase_order = response.data[0]
                        print(f"✅ Found in Supabase!")
            except Exception as sup_err:
                print(f"⚠️ Supabase lookup error (despite DNS UP): {sup_err}")
        else:
            print(f"🌐 Supabase unreachable (DNS down), skipping cloud lookup.")

        if supabase_order:
            return jsonify({
                "success": True,
                "order": supabase_order,
                "audio_url": supabase_order.get("audio_file_url"),
                "frame_title": supabase_order.get("frame_title")
            })
        
        # 2. Fallback to local orders list
        print(f"🔍 Checking local backup for scan_id: {scan_id}")
        local_order = next((o for o in orders if o.get('scan_id') == scan_id or str(o.get('id')) == scan_id), None)
        if local_order:
            print(f"✅ Found in local backup!")
            return jsonify({
                "success": True,
                "order": local_order,
                "audio_url": local_order.get("audio_file_url"),
                "frame_title": local_order.get("frame_title")
            })
        
        return jsonify({"success": False, "error": "Order not found"}), 404
        
    except Exception as e:
        print(f"❌ Scan lookup error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Supabase Docker API with Spotify Waveform Code Generation...")
    print("📡 Available endpoints:")
    print("  GET  /api/frames/           - List all frames")
    print("  GET  /api/frames/{id}/      - Get specific frame")
    print("  GET  /api/orders/            - List orders from Supabase")
    print("  POST /api/orders/            - Create order with audio upload & Spotify waveform code")
    print("  PUT  /api/orders/{id}        - Update order details")
    print("  DELETE /api/orders/{id}      - Delete order")
    print("  PUT  /api/orders/{id}/status - Update order status & agent")
    print("  GET  /api/confirmation-agents/ - List agents")
    print("  POST /api/confirmation-agents/ - Add agent")
    print("  GET  /api/audio/{id}/         - Scan frame Spotify waveform code")
    print("  POST /api/track-play/{id}/   - Track audio play")
    print("  GET  /api/statistics/        - Get statistics")
    print("  GET  /api/test-storage/      - Test Supabase Storage connection")
    print("  GET  /health/                 - Health check (includes storage status)")
    print(f"\n🌐 Server running on http://localhost:8001")
    print(f"🔗 Supabase URL: {SUPABASE_URL}")
    print(f"🎵 Spotify waveform codes will be generated automatically for audio uploads!")
    print(f"📦 Waveform codes are stored in Supabase Storage (wave_codes bucket)")
    print(f"📱 Mobile app can scan waveform codes to play recorded audio")
    print(f"\n⚠️  IMPORTANT Setup:")
    print(f"   1. Create 'wave_codes' bucket in Supabase Storage Dashboard")
    print(f"      → Go to Storage → Create bucket → Name: 'wave_codes' → Set PUBLIC")
    print(f"   2. Create 'api_order' table with columns: audio_file_url, qr_code_url, qr_code_data")
    print(f"   3. Test storage: GET http://localhost:8001/api/test-storage/")
    print(f"   4. Check health: GET http://localhost:8001/health/")
    
    # Disable debug mode to avoid reloader issues
    app.run(host='0.0.0.0', port=8001, debug=False)
