#!/usr/bin/env python3
"""
Test script for Django Audio Waveform Generator
"""

import sys
import os
import requests
import json

# Add the django_waveform_generator to path
sys.path.append('django_waveform_generator')

def test_waveform_service():
    """Test the waveform service directly"""
    print("🎵 Testing Django Audio Waveform Generator")
    print("=" * 50)
    
    try:
        from waveform_service import SpotifyWaveformGenerator, generate_waveform_code
        
        # Test with a sample audio URL (you can replace with a real audio file)
        test_audio_url = "https://www.soundjay.com/misc/sounds/bell-ringing-05.wav"
        
        print(f"Testing with audio URL: {test_audio_url}")
        
        # Create generator instance
        generator = SpotifyWaveformGenerator(
            width=800,
            height=200,
            bar_count=60,
            bar_width=8,
            bar_spacing=4
        )
        
        # Test waveform generation
        print("Generating waveform code...")
        waveform_url = generate_waveform_code(test_audio_url, "test_waveform")
        
        print(f"✅ Generated waveform URL: {waveform_url}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install -r django_waveform_generator/requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints (requires Django server running)"""
    print("\n🌐 Testing API Endpoints")
    print("=" * 30)
    
    base_url = "http://localhost:8000/api/audio"
    
    # Test endpoints
    endpoints = [
        ("GET", f"{base_url}/", "List audio files"),
        ("GET", f"{base_url}/waveform_stats/", "Waveform statistics"),
    ]
    
    for method, url, description in endpoints:
        try:
            print(f"Testing {description}...")
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print(f"  ✅ {method} {url} - OK")
            else:
                print(f"  ⚠️  {method} {url} - Status: {response.status_code}")
                
        except requests.ConnectionError:
            print(f"  ❌ {method} {url} - Connection failed (Django server not running)")
        except Exception as e:
            print(f"  ❌ {method} {url} - Error: {e}")

def test_audio_upload():
    """Test audio upload with waveform generation"""
    print("\n📤 Testing Audio Upload")
    print("=" * 25)
    
    # Example audio upload data
    upload_data = {
        "title": "Test Audio File",
        "audio_url": "https://www.soundjay.com/misc/sounds/bell-ringing-05.wav"
    }
    
    print("Example upload data:")
    print(json.dumps(upload_data, indent=2))
    
    print("\nTo test upload, use this curl command:")
    print("curl -X POST http://localhost:8000/api/audio/ \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -H 'Authorization: Bearer YOUR_TOKEN' \\")
    print("  -d '{\"title\": \"Test Audio\", \"audio_url\": \"https://example.com/audio.mp3\"}'")

def show_integration_guide():
    """Show integration guide"""
    print("\n📋 Integration Guide")
    print("=" * 20)
    
    print("""
1. Add to your Django project:
   - Copy django_waveform_generator/ to your project
   - Add to INSTALLED_APPS in settings.py
   - Add Supabase configuration
   - Run migrations

2. API Usage:
   POST /api/audio/
   {
     "title": "My Audio",
     "audio_url": "https://example.com/audio.mp3"
   }

3. Generated Response:
   {
     "id": "uuid",
     "title": "My Audio",
     "audio_url": "https://example.com/audio.mp3",
     "code_image": "https://supabase.co/storage/wave_codes/waveform_uuid.png",
     "has_waveform_code": true,
     "waveform_code_url": "https://supabase.co/storage/wave_codes/waveform_uuid.png"
   }

4. Additional Endpoints:
   - POST /api/audio/{id}/regenerate_waveform/ - Regenerate waveform
   - GET /api/audio/{id}/waveform_image/ - Get waveform URL
   - GET /api/audio/waveform_stats/ - Get statistics
""")

if __name__ == "__main__":
    print("Django Audio Waveform Generator - Test Suite")
    print("=" * 60)
    
    # Test waveform service
    service_ok = test_waveform_service()
    
    # Test API endpoints
    test_api_endpoints()
    
    # Test audio upload
    test_audio_upload()
    
    # Show integration guide
    show_integration_guide()
    
    print("\n" + "=" * 60)
    if service_ok:
        print("🎉 Waveform service is working!")
        print("Ready for integration with your Django project.")
    else:
        print("❌ Waveform service has issues.")
        print("Check dependencies and configuration.")
    print("=" * 60)
