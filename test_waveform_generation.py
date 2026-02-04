#!/usr/bin/env python3
"""
Test script for waveform generation without Django
"""

import sys
import os
sys.path.append('django_audio_waveform')

from waveform_generator import SpotifyWaveformGenerator
import uuid

def test_waveform_generation():
    """Test waveform generation with different parameters"""
    
    print("🎵 Testing Spotify-Style Waveform Generation")
    print("=" * 50)
    
    # Test different configurations
    configs = [
        {"width": 800, "height": 200, "bar_width": 2, "bar_spacing": 1},
        {"width": 400, "height": 100, "bar_width": 1, "bar_spacing": 1},
        {"width": 1200, "height": 300, "bar_width": 3, "bar_spacing": 2},
    ]
    
    # Generate test audio IDs
    test_ids = [
        str(uuid.uuid4()),
        str(uuid.uuid4()),
        "test-audio-123",
        "same-id-test",
        "same-id-test",  # Same ID to test reproducibility
    ]
    
    for i, config in enumerate(configs):
        print(f"\n📊 Configuration {i+1}: {config}")
        
        generator = SpotifyWaveformGenerator(**config)
        
        for j, audio_id in enumerate(test_ids):
            # Generate waveform
            waveform_bytes = generator.generate_waveform_bytes(
                "fake_audio_path.mp3",  # Fake path for testing
                audio_id
            )
            
            # Save to file
            filename = f"waveform_config{i+1}_id{j+1}_{audio_id[:8]}.png"
            with open(filename, "wb") as f:
                f.write(waveform_bytes)
            
            print(f"  ✅ Generated: {filename} ({len(waveform_bytes)} bytes)")
    
    # Test reproducibility
    print(f"\n🔄 Testing Reproducibility:")
    generator = SpotifyWaveformGenerator()
    test_id = "reproducibility-test"
    
    # Generate same waveform twice
    waveform1 = generator.generate_waveform_bytes("fake.mp3", test_id)
    waveform2 = generator.generate_waveform_bytes("fake.mp3", test_id)
    
    are_identical = waveform1 == waveform2
    print(f"  Same ID generates identical waveform: {are_identical}")
    
    # Test different IDs generate different waveforms
    waveform3 = generator.generate_waveform_bytes("fake.mp3", "different-id")
    are_different = waveform1 != waveform3
    print(f"  Different IDs generate different waveforms: {are_different}")
    
    print(f"\n🎉 Test completed! Check the generated PNG files.")
    print(f"   Files created: {len([f for f in os.listdir('.') if f.startswith('waveform_')])}")

def test_real_audio_analysis():
    """Test real audio analysis if librosa is available"""
    
    print(f"\n🎧 Testing Real Audio Analysis:")
    
    try:
        from waveform_generator import RealAudioWaveformGenerator
        
        generator = RealAudioWaveformGenerator()
        print("  ✅ RealAudioWaveformGenerator available")
        print("  📝 Note: Requires actual audio file for testing")
        
    except ImportError:
        print("  ⚠️  librosa not available - using simulated waveforms only")
        print("  📝 Install with: pip install librosa")

if __name__ == "__main__":
    test_waveform_generation()
    test_real_audio_analysis()
