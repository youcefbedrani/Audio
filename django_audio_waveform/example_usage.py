#!/usr/bin/env python3
"""
Example usage of Django Audio Waveform Generator
"""

import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from django_audio_waveform.models import Audio
from django_audio_waveform.waveform_generator import SpotifyWaveformGenerator
from django.core.files.uploadedfile import SimpleUploadedFile

def example_upload_and_generate():
    """Example of uploading audio and generating waveform"""
    
    # Create a test audio file (in real usage, this would come from user upload)
    test_audio_content = b"fake audio content for testing"
    audio_file = SimpleUploadedFile(
        "test_audio.mp3",
        test_audio_content,
        content_type="audio/mpeg"
    )
    
    # Create Audio instance
    audio = Audio.objects.create(
        title="Test Audio Track",
        audio_file=audio_file
    )
    
    print(f"Created audio: {audio.title} (ID: {audio.id})")
    
    # Generate waveform
    generator = SpotifyWaveformGenerator(width=800, height=200)
    waveform_bytes = generator.generate_waveform_bytes(
        audio.audio_file.path,
        str(audio.id)
    )
    
    # Save waveform locally for testing
    waveform_path = f"waveform_{audio.id}.png"
    with open(waveform_path, "wb") as f:
        f.write(waveform_bytes)
    
    print(f"Generated waveform: {waveform_path}")
    print(f"Waveform size: {len(waveform_bytes)} bytes")
    
    return audio

def example_reproducible_waveform():
    """Demonstrate that waveforms are reproducible"""
    
    audio_id = "123e4567-e89b-12d3-a456-426614174000"
    generator = SpotifyWaveformGenerator()
    
    # Generate waveform multiple times with same ID
    waveform1 = generator.generate_waveform_bytes("fake_path.mp3", audio_id)
    waveform2 = generator.generate_waveform_bytes("fake_path.mp3", audio_id)
    
    # They should be identical
    are_identical = waveform1 == waveform2
    print(f"Waveforms are reproducible: {are_identical}")
    
    return are_identical

def example_api_usage():
    """Example of how to use the API endpoints"""
    
    print("API Usage Examples:")
    print("=" * 50)
    
    print("\n1. Upload Audio File:")
    print("POST /api/audio/")
    print("Content-Type: multipart/form-data")
    print("Body: {")
    print("  'title': 'My Audio Track',")
    print("  'audio_file': <file>")
    print("}")
    
    print("\n2. Get Audio Details:")
    print("GET /api/audio/{id}/")
    
    print("\n3. Regenerate Waveform:")
    print("POST /api/audio/{id}/regenerate_waveform/")
    
    print("\n4. Get Waveform Image URL:")
    print("GET /api/audio/{id}/waveform_image/")
    
    print("\n5. List All Audio Files:")
    print("GET /api/audio/")

def example_flutter_integration():
    """Example Flutter code for integration"""
    
    flutter_code = '''
// Flutter integration example
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import 'dart:io';
import 'dart:convert';

class AudioWaveformService {
  static const String baseUrl = 'https://your-api.com/api';
  
  // Upload audio file
  static Future<Map<String, dynamic>> uploadAudio({
    required String title,
    required File audioFile,
  }) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/audio/'),
    );
    
    request.fields['title'] = title;
    request.files.add(
      await http.MultipartFile.fromPath(
        'audio_file',
        audioFile.path,
        contentType: MediaType('audio', 'mpeg'),
      ),
    );
    
    var response = await request.send();
    var responseData = await response.stream.bytesToString();
    
    if (response.statusCode == 201) {
      return json.decode(responseData);
    } else {
      throw Exception('Failed to upload audio');
    }
  }
  
  // Get waveform image URL
  static Future<String> getWaveformImageUrl(String audioId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/audio/$audioId/waveform_image/'),
    );
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['image_url'];
    } else {
      throw Exception('Failed to get waveform image');
    }
  }
}

// Widget to display waveform
class WaveformDisplay extends StatelessWidget {
  final String waveformUrl;
  
  const WaveformDisplay({
    Key? key,
    required this.waveformUrl,
  }) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return Container(
      width: 800,
      height: 200,
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(8),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 4,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(8),
        child: Image.network(
          waveformUrl,
          fit: BoxFit.cover,
          errorBuilder: (context, error, stackTrace) {
            return Center(
              child: Text('Failed to load waveform'),
            );
          },
        ),
      ),
    );
  }
}
'''
    
    print("Flutter Integration Example:")
    print("=" * 50)
    print(flutter_code)

if __name__ == "__main__":
    print("Django Audio Waveform Generator - Example Usage")
    print("=" * 60)
    
    # Run examples
    try:
        # Example 1: Upload and generate
        print("\n1. Upload and Generate Waveform:")
        audio = example_upload_and_generate()
        
        # Example 2: Reproducible waveforms
        print("\n2. Test Reproducible Waveforms:")
        example_reproducible_waveform()
        
        # Example 3: API usage
        print("\n3. API Usage Examples:")
        example_api_usage()
        
        # Example 4: Flutter integration
        print("\n4. Flutter Integration:")
        example_flutter_integration()
        
        print("\n" + "=" * 60)
        print("✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        sys.exit(1)
