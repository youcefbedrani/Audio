# Django Audio Waveform Generator - Complete Integration Guide

## 🎵 Spotify-Style Waveform Code Generator for Django

This guide shows you how to integrate the Django Audio Waveform Generator into your existing Django project to automatically generate Spotify-style waveform codes from uploaded audio files.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r django_waveform_generator/requirements.txt
```

### 2. Add to Django Settings

In your `settings.py`:

```python
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ... your existing apps
    'rest_framework',
    'django_waveform_generator',
]

# Supabase Configuration
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your-anon-key"

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50MB
```

### 3. Add URLs

In your main `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    # ... your existing URLs
    path('api/', include('django_waveform_generator.urls')),
]
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Supabase Storage Bucket

1. Go to your Supabase dashboard
2. Navigate to Storage
3. Create a new bucket named `wave_codes`
4. Set it to public

## 📱 API Usage

### Upload Audio with Waveform Generation

```http
POST /api/audio/
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN

{
    "title": "My Audio Track",
    "audio_url": "https://example.com/audio.mp3"
}
```

**Response:**
```json
{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "My Audio Track",
    "audio_file": null,
    "audio_url": "https://example.com/audio.mp3",
    "code_image": "https://your-project.supabase.co/storage/v1/object/public/wave_codes/waveform_123e4567.png",
    "has_waveform_code": true,
    "waveform_code_url": "https://your-project.supabase.co/storage/v1/object/public/wave_codes/waveform_123e4567.png",
    "created_at": "2023-12-01T10:00:00Z",
    "updated_at": "2023-12-01T10:00:00Z"
}
```

### Regenerate Waveform Code

```http
POST /api/audio/{id}/regenerate_waveform/
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN

{
    "force_regenerate": true
}
```

### Get Waveform Image URL

```http
GET /api/audio/{id}/waveform_image/
Authorization: Bearer YOUR_TOKEN
```

### Get Statistics

```http
GET /api/audio/waveform_stats/
Authorization: Bearer YOUR_TOKEN
```

## 🎨 Waveform Customization

### Customize Waveform Appearance

```python
from django_waveform_generator.waveform_service import SpotifyWaveformGenerator

# Create custom generator
generator = SpotifyWaveformGenerator(
    width=800,        # Image width in pixels
    height=200,       # Image height in pixels
    bar_count=60,     # Number of bars
    bar_width=8,      # Width of each bar
    bar_spacing=4     # Space between bars
)

# Generate waveform
waveform_url = generator.generate_waveform_code(
    audio_url="https://example.com/audio.mp3",
    output_name="custom_waveform"
)
```

### Different Waveform Styles

```python
# Minimal style
minimal_generator = SpotifyWaveformGenerator(
    width=400, height=100, bar_count=30, bar_width=4, bar_spacing=2
)

# Detailed style
detailed_generator = SpotifyWaveformGenerator(
    width=1200, height=300, bar_count=80, bar_width=10, bar_spacing=6
)
```

## 🔧 Management Commands

### Generate Waveforms for Existing Audio

```bash
# Generate waveforms for all audio files without them
python manage.py generate_waveforms

# Generate for specific audio file
python manage.py generate_waveforms --audio-id 123e4567-e89b-12d3-a456-426614174000

# Force regeneration of existing waveforms
python manage.py generate_waveforms --force

# Limit number of files to process
python manage.py generate_waveforms --limit 5
```

## 🧪 Testing

### Test the Waveform Service

```bash
python test_django_waveform.py
```

### Test API Endpoints

```bash
# Test health check
curl http://localhost:8000/api/audio/waveform_stats/

# Test audio upload
curl -X POST http://localhost:8000/api/audio/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"title": "Test Audio", "audio_url": "https://example.com/audio.mp3"}'
```

## 📊 Flutter Integration

### Upload Audio and Get Waveform

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class AudioWaveformService {
  static const String baseUrl = 'https://your-api.com/api';
  
  static Future<Map<String, dynamic>> uploadAudio({
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
  
  static Future<String> getWaveformImageUrl({
    required String audioId,
    required String authToken,
  }) async {
    final response = await http.get(
      Uri.parse('$baseUrl/audio/$audioId/waveform_image/'),
      headers: {
        'Authorization': 'Bearer $authToken',
      },
    );
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['waveform_url'];
    } else {
      throw Exception('Failed to get waveform image');
    }
  }
}
```

### Display Waveform in Flutter

```dart
import 'package:flutter/material.dart';

class WaveformDisplay extends StatelessWidget {
  final String waveformUrl;
  final double width;
  final double height;
  
  const WaveformDisplay({
    Key? key,
    required this.waveformUrl,
    this.width = 800,
    this.height = 200,
  }) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return Container(
      width: width,
      height: height,
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
              child: CircularProgressIndicator(
                value: loadingProgress.expectedTotalBytes != null
                    ? loadingProgress.cumulativeBytesLoaded / 
                      loadingProgress.expectedTotalBytes!
                    : null,
              ),
            );
          },
          errorBuilder: (context, error, stackTrace) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.error, color: Colors.red),
                  Text('Failed to load waveform'),
                ],
              ),
            );
          },
        ),
      ),
    );
  }
}
```

## 🔍 Troubleshooting

### Common Issues

1. **Supabase Upload Fails**
   - Check bucket permissions
   - Verify credentials
   - Ensure bucket exists and is public

2. **Audio Analysis Fails**
   - Check if audio URL is accessible
   - Verify audio format (MP3, WAV supported)
   - Check librosa installation

3. **Waveform Not Generated**
   - Check logs for errors
   - Verify audio_url is provided
   - Test with management command

4. **Permission Errors**
   - Check authentication
   - Verify user permissions
   - Check API endpoint access

### Debug Mode

Enable detailed logging:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'waveform_generation.log',
        },
    },
    'loggers': {
        'django_waveform_generator': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

## 📁 File Structure

```
django_waveform_generator/
├── __init__.py
├── apps.py
├── models.py
├── views.py
├── serializers.py
├── urls.py
├── admin.py
├── waveform_service.py
├── requirements.txt
├── settings_example.py
├── management/
│   └── commands/
│       └── generate_waveforms.py
└── README.md
```

## 🎯 Features

- ✅ **Automatic Waveform Generation**: Generates on audio upload
- ✅ **Spotify-Style Design**: Clean, professional waveform codes
- ✅ **Supabase Integration**: Uploads images to cloud storage
- ✅ **Reproducible**: Same audio = same waveform pattern
- ✅ **Customizable**: Configurable dimensions and appearance
- ✅ **REST API**: Full CRUD operations with DRF
- ✅ **Management Commands**: Bulk processing and regeneration
- ✅ **Error Handling**: Graceful fallbacks and logging
- ✅ **Flutter Ready**: Complete mobile app integration

## 🚀 Production Ready

The solution is production-ready with:
- Comprehensive error handling
- Logging and monitoring
- Configurable settings
- Security considerations
- Performance optimizations
- Clean, modular code

Your Django API now automatically generates beautiful Spotify-style waveform codes for every uploaded audio file! 🎵✨
