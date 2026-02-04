#!/usr/bin/env python3
"""
Complete Integration Example for Spotify-Style Waveform Codes
Shows how to integrate with your existing Django API and Supabase
"""

def show_django_integration():
    """Show Django integration example"""
    
    django_integration = '''
# 1. Add to your Django models.py

from django.db import models
import uuid

class Audio(models.Model):
    """
    Your existing Audio model with Spotify waveform code support
    """
    # Your existing fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='audio_files/')
    audio_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # NEW: Spotify waveform code fields
    code_image = models.URLField(
        blank=True, 
        null=True, 
        help_text="Supabase URL of the generated Spotify waveform code image"
    )
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.id})"
    
    @property
    def has_spotify_waveform(self):
        """Check if Spotify waveform code exists."""
        return bool(self.code_image)

# 2. Add to your Django views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from django_spotify_waveform_service import generate_spotify_waveform_code
import logging

logger = logging.getLogger(__name__)

class AudioViewSet(viewsets.ModelViewSet):
    """
    Your existing Audio ViewSet with Spotify waveform generation
    """
    
    def create(self, request, *args, **kwargs):
        """
        Handle audio file upload and automatically generate Spotify waveform code.
        """
        # Your existing audio creation logic
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create the audio instance
        audio = serializer.save()
        
        # NEW: Generate Spotify waveform code if audio_url is provided
        if hasattr(audio, 'audio_url') and audio.audio_url:
            try:
                waveform_url = generate_spotify_waveform_code(
                    audio_url=audio.audio_url,
                    output_name=f"spotify_waveform_{audio.id}"
                )
                
                # Save the waveform URL to your model
                audio.code_image = waveform_url
                audio.save()
                
                logger.info(f"Generated Spotify waveform code for audio {audio.id}: {waveform_url}")
                
            except Exception as e:
                logger.error(f"Failed to generate Spotify waveform for audio {audio.id}: {str(e)}")
                # Don't fail the request, just log the error
        
        # Return response with waveform URL included
        response_serializer = self.get_serializer(audio)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

# 3. Add to your Django settings.py

INSTALLED_APPS = [
    # ... your existing apps
    'rest_framework',
    'django_spotify_waveform',  # Your app name
]

# Supabase Configuration
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your-anon-key"

# 4. Add to your main urls.py

urlpatterns = [
    # ... your existing URLs
    path('api/audio/', include('your_app.urls')),  # Your audio URLs
]
'''
    
    print("Django Integration Example:")
    print("=" * 40)
    print(django_integration)

def show_api_usage():
    """Show API usage examples"""
    
    api_examples = '''
# API Usage Examples

# 1. Upload audio and get Spotify waveform code
curl -X POST http://localhost:8000/api/audio/ \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer YOUR_TOKEN" \\
  -d '{
    "title": "My Audio Track",
    "audio_url": "https://example.com/audio.mp3"
  }'

# Response will include:
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "My Audio Track",
  "audio_url": "https://example.com/audio.mp3",
  "code_image": "https://your-project.supabase.co/storage/v1/object/public/wave_codes/spotify_waveform_123e4567.png",
  "has_spotify_waveform": true,
  "created_at": "2023-12-01T10:00:00Z",
  "updated_at": "2023-12-01T10:00:00Z"
}

# 2. Regenerate Spotify waveform code
curl -X POST http://localhost:8000/api/audio/123e4567-e89b-12d3-a456-426614174000/regenerate_waveform/ \\
  -H "Authorization: Bearer YOUR_TOKEN" \\
  -d '{"force_regenerate": true}'

# 3. Get Spotify waveform image URL
curl http://localhost:8000/api/audio/123e4567-e89b-12d3-a456-426614174000/waveform_image/ \\
  -H "Authorization: Bearer YOUR_TOKEN"

# 4. Get statistics
curl http://localhost:8000/api/audio/waveform_stats/ \\
  -H "Authorization: Bearer YOUR_TOKEN"
'''
    
    print("\nAPI Usage Examples:")
    print("=" * 30)
    print(api_examples)

def show_flutter_integration():
    """Show Flutter integration example"""
    
    flutter_code = '''
// Flutter integration for Spotify waveform codes

import 'package:http/http.dart' as http;
import 'dart:convert';

class SpotifyWaveformService {
  static const String baseUrl = 'https://your-api.com/api';
  
  // Upload audio and get Spotify waveform code
  static Future<Map<String, dynamic>> uploadAudioWithSpotifyWaveform({
    required String title,
    required String audioUrl,
    required String authToken,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/audio/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $authToken',
      },
      body: json.encode({
        'title': title,
        'audio_url': audioUrl,
      }),
    );
    
    if (response.statusCode == 201) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to upload audio: ${response.statusCode}');
    }
  }
  
  // Display Spotify waveform code widget
  Widget buildSpotifyWaveformDisplay(String waveformUrl) {
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
          loadingBuilder: (context, child, loadingProgress) {
            if (loadingProgress == null) return child;
            return Center(
              child: CircularProgressIndicator(),
            );
          },
          errorBuilder: (context, error, stackTrace) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.music_note, color: Colors.grey),
                  Text('Spotify Waveform Code'),
                  Text('Failed to load', style: TextStyle(color: Colors.red)),
                ],
              ),
            );
          },
        ),
      ),
    );
  }
}

// Usage in your Flutter app
class AudioUploadScreen extends StatefulWidget {
  @override
  _AudioUploadScreenState createState() => _AudioUploadScreenState();
}

class _AudioUploadScreenState extends State<AudioUploadScreen> {
  String? waveformUrl;
  bool isLoading = false;
  
  Future<void> uploadAudio(String title, String audioUrl) async {
    setState(() {
      isLoading = true;
    });
    
    try {
      final result = await SpotifyWaveformService.uploadAudioWithSpotifyWaveform(
        title: title,
        audioUrl: audioUrl,
        authToken: "your_token",
      );
      
      setState(() {
        waveformUrl = result['code_image'];
        isLoading = false;
      });
      
    } catch (e) {
      setState(() {
        isLoading = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Upload failed: $e')),
      );
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Spotify Waveform Generator'),
        backgroundColor: Colors.green,
      ),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          children: [
            if (isLoading)
              CircularProgressIndicator()
            else if (waveformUrl != null) ...[
              Text('Spotify Waveform Code:', style: Theme.of(context).textTheme.headline6),
              SizedBox(height: 16),
              SpotifyWaveformService.buildSpotifyWaveformDisplay(waveformUrl!),
              SizedBox(height: 16),
              Text('This is your Spotify-style waveform code!'),
            ] else
              Text('Upload an audio file to generate a Spotify waveform code'),
          ],
        ),
      ),
    );
  }
}
'''
    
    print("\nFlutter Integration Example:")
    print("=" * 40)
    print(flutter_code)

def show_supabase_setup():
    """Show Supabase setup instructions"""
    
    supabase_setup = '''
# Supabase Setup Instructions

## 1. Create Storage Bucket
1. Go to your Supabase dashboard
2. Navigate to Storage
3. Click "Create a new bucket"
4. Name: "wave_codes"
5. Set to PUBLIC (so images can be accessed via URL)
6. Click "Create bucket"

## 2. Configure Bucket Permissions
1. Go to Storage > wave_codes bucket
2. Click "Settings" tab
3. Under "Policies", add a new policy:
   - Policy name: "Public read access"
   - Policy definition: 
     ```sql
     CREATE POLICY "Public read access" ON storage.objects
     FOR SELECT USING (bucket_id = 'wave_codes');
     ```

## 3. Test Upload
You can test the upload with this Python script:

```python
from supabase import create_client, Client

# Initialize Supabase client
supabase: Client = create_client(
    "https://your-project.supabase.co",
    "your-anon-key"
)

# Test upload
with open("test_waveform.png", "rb") as f:
    result = supabase.storage.from_("wave_codes").upload(
        "test_waveform.png",
        f.read(),
        file_options={"content-type": "image/png"}
    )

if result.get('error'):
    print(f"Upload failed: {result['error']}")
else:
    # Get public URL
    public_url = supabase.storage.from_("wave_codes").get_public_url("test_waveform.png")
    print(f"Upload successful: {public_url}")
```
'''
    
    print("\nSupabase Setup Instructions:")
    print("=" * 35)
    print(supabase_setup)

def show_spotify_waveform_features():
    """Show Spotify waveform features"""
    
    features = '''
# Spotify Waveform Code Features

## ✅ What You Get:
- **Authentic Spotify Style**: Vertical bars with varying heights (NOT QR codes)
- **Real Audio Analysis**: Uses librosa to analyze actual audio waveforms
- **Supabase Storage**: Uploads to your 'wave_codes' bucket
- **Reproducible**: Same audio always generates same waveform pattern
- **Customizable**: Different sizes and bar configurations
- **Production Ready**: Error handling, logging, fallbacks

## 🎵 Waveform Characteristics:
- **White Background**: Clean, professional look
- **Black Vertical Bars**: Variable height based on audio amplitude
- **Rounded Ends**: Smooth, modern appearance
- **Centered Layout**: Balanced visual design
- **60 Bars Default**: Standard Spotify-style configuration
- **800x200px Default**: Optimal size for mobile apps

## 📱 Perfect for:
- Music streaming apps
- Audio sharing platforms
- Podcast applications
- Voice message apps
- Any app that needs audio visualization

## 🔗 Reference:
Based on authentic Spotify codes: https://free-barcode.com/barcode/barcode-history/history-spotify-codes/1.jpg
'''
    
    print("\nSpotify Waveform Code Features:")
    print("=" * 40)
    print(features)

if __name__ == "__main__":
    print("🎵 Complete Spotify Waveform Code Integration")
    print("=" * 60)
    print("Generates authentic Spotify-style waveform codes (vertical bars)")
    print("NOT QR codes - these are audio waveform visualizations")
    print("=" * 60)
    
    # Show all integration examples
    show_django_integration()
    show_api_usage()
    show_flutter_integration()
    show_supabase_setup()
    show_spotify_waveform_features()
    
    print("\n" + "=" * 60)
    print("🎉 Integration complete!")
    print("Your Django API now generates authentic Spotify waveform codes!")
    print("Ready for your 'wave_codes' Supabase bucket!")
    print("=" * 60)
