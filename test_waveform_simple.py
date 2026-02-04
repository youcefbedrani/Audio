#!/usr/bin/env python3
"""
Simple test for waveform generation without Supabase
"""

import sys
import os
import io
import numpy as np
from PIL import Image, ImageDraw

# Add the django_waveform_generator to path
sys.path.append('django_waveform_generator')

def test_waveform_generation():
    """Test waveform generation without Supabase upload"""
    print("🎵 Testing Waveform Generation (Local Only)")
    print("=" * 50)
    
    try:
        from waveform_service import SpotifyWaveformGenerator
        
        # Create generator instance
        generator = SpotifyWaveformGenerator(
            width=800,
            height=200,
            bar_count=60,
            bar_width=8,
            bar_spacing=4
        )
        
        # Test with fallback waveform (no audio URL needed)
        print("Generating test waveform...")
        
        # Generate fallback waveform data
        waveform_data = generator._generate_fallback_waveform()
        print(f"Generated waveform data: {len(waveform_data)} bars")
        
        # Create waveform image
        image_bytes = generator._create_waveform_image(waveform_data)
        print(f"Generated image: {len(image_bytes)} bytes")
        
        # Save to file
        with open("test_waveform_output.png", "wb") as f:
            f.write(image_bytes)
        
        print("✅ Waveform image saved as: test_waveform_output.png")
        
        # Test different configurations
        configs = [
            {"width": 400, "height": 100, "bar_count": 30, "bar_width": 4, "bar_spacing": 2},
            {"width": 1200, "height": 300, "bar_count": 80, "bar_width": 10, "bar_spacing": 6},
        ]
        
        for i, config in enumerate(configs):
            print(f"\nTesting configuration {i+1}: {config}")
            test_generator = SpotifyWaveformGenerator(**config)
            test_data = test_generator._generate_fallback_waveform()
            test_image = test_generator._create_waveform_image(test_data)
            
            filename = f"test_waveform_config_{i+1}.png"
            with open(filename, "wb") as f:
                f.write(test_image)
            
            print(f"  ✅ Saved: {filename} ({len(test_image)} bytes)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_audio_analysis():
    """Test audio analysis with librosa"""
    print("\n🎧 Testing Audio Analysis")
    print("=" * 30)
    
    try:
        import librosa
        print("✅ librosa imported successfully")
        
        # Test with a simple audio generation
        # Generate a test audio signal
        sr = 22050  # Sample rate
        duration = 5  # seconds
        t = np.linspace(0, duration, sr * duration)
        
        # Create a test signal with multiple frequencies
        audio_signal = (np.sin(2 * np.pi * 440 * t) +  # 440 Hz
                       0.5 * np.sin(2 * np.pi * 880 * t) +  # 880 Hz
                       0.3 * np.sin(2 * np.pi * 1320 * t))  # 1320 Hz
        
        # Add some noise
        audio_signal += 0.1 * np.random.randn(len(audio_signal))
        
        print(f"Generated test audio: {len(audio_signal)} samples")
        
        # Test librosa analysis
        rms = librosa.feature.rms(y=audio_signal)[0]
        print(f"RMS analysis: {len(rms)} frames")
        
        # Test spectral analysis
        spectral_centroids = librosa.feature.spectral_centroid(y=audio_signal, sr=sr)[0]
        print(f"Spectral centroids: {len(spectral_centroids)} frames")
        
        print("✅ Audio analysis working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Audio analysis error: {e}")
        return False

def show_integration_example():
    """Show integration example"""
    print("\n📋 Integration Example")
    print("=" * 25)
    
    print("""
# In your Django view or service:

from django_waveform_generator.waveform_service import generate_waveform_code

def process_audio_upload(audio_url, audio_id):
    try:
        # Generate waveform code
        waveform_url = generate_waveform_code(
            audio_url=audio_url,
            output_name=f"waveform_{audio_id}"
        )
        
        # Save to your model
        audio = Audio.objects.get(id=audio_id)
        audio.code_image = waveform_url
        audio.save()
        
        return waveform_url
        
    except Exception as e:
        logger.error(f"Failed to generate waveform: {e}")
        return None
""")

if __name__ == "__main__":
    print("Django Audio Waveform Generator - Simple Test")
    print("=" * 60)
    
    # Test waveform generation
    waveform_ok = test_waveform_generation()
    
    # Test audio analysis
    audio_ok = test_audio_analysis()
    
    # Show integration example
    show_integration_example()
    
    print("\n" + "=" * 60)
    if waveform_ok and audio_ok:
        print("🎉 All tests passed! Waveform generation is working.")
        print("Ready for integration with your Django project.")
    else:
        print("❌ Some tests failed. Check the errors above.")
    print("=" * 60)
