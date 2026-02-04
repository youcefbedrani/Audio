# Django Audio Waveform Integration Guide

## 🎵 Complete Django + Supabase Backend for Flutter Mobile App

This guide shows you how to integrate the Django Audio Waveform Generator into your existing project.

## 📁 Project Structure

```
your_project/
├── django_audio_waveform/          # The audio waveform app
│   ├── models.py                   # Audio model with waveform fields
│   ├── views.py                    # API endpoints for upload/generation
│   ├── serializers.py              # DRF serializers
│   ├── waveform_generator.py       # Spotify-style waveform generator
│   ├── urls.py                     # URL routing
│   └── requirements.txt            # Dependencies
├── your_main_app/
│   ├── settings.py                 # Add configuration here
│   └── urls.py                     # Include waveform URLs
└── manage.py
```

## 🚀 Quick Setup

### 1. Copy the Django App

```bash
# Copy the django_audio_waveform folder to your Django project
cp -r django_audio_waveform/ /path/to/your/django/project/
```

### 2. Install Dependencies

```bash
pip install -r django_audio_waveform/requirements.txt
```

### 3. Update Django Settings

Add to your `settings.py`:

```python
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ... your existing apps
    'rest_framework',
    'django_audio_waveform',
]

# Supabase Configuration
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your-anon-key"

# Cloudinary Configuration  
CLOUDINARY_CLOUD_NAME = "your-cloud-name"
CLOUDINARY_API_KEY = "your-api-key"
CLOUDINARY_API_SECRET = "your-api-secret"

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

### 4. Update Main URLs

In your main `urls.py`:

```python
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your existing URLs
    path('api/', include('django_audio_waveform.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Supabase Storage Bucket

1. Go to your Supabase dashboard
2. Navigate to Storage
3. Create a new bucket named `wave_codes`
4. Set it to public

## 📱 Flutter Integration

### 1. Upload Audio File

```dart
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import 'dart:io';
import 'dart:convert';

class AudioWaveformService {
  static const String baseUrl = 'https://your-api.com/api';
  
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
      throw Exception('Failed to upload audio: ${response.statusCode}');
    }
  }
}
```

### 2. Display Waveform

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

### 3. Complete Example Screen

```dart
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';

class AudioUploadScreen extends StatefulWidget {
  @override
  _AudioUploadScreenState createState() => _AudioUploadScreenState();
}

class _AudioUploadScreenState extends State<AudioUploadScreen> {
  final _titleController = TextEditingController();
  File? _audioFile;
  Map<String, dynamic>? _uploadResult;
  bool _isUploading = false;

  Future<void> _pickAudioFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.audio,
    );

    if (result != null) {
      setState(() {
        _audioFile = File(result.files.first.path!);
      });
    }
  }

  Future<void> _uploadAudio() async {
    if (_audioFile == null || _titleController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Please select an audio file and enter a title')),
      );
      return;
    }

    setState(() {
      _isUploading = true;
    });

    try {
      final result = await AudioWaveformService.uploadAudio(
        title: _titleController.text,
        audioFile: _audioFile!,
      );

      setState(() {
        _uploadResult = result;
        _isUploading = false;
      });

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Audio uploaded successfully!')),
      );
    } catch (e) {
      setState(() {
        _isUploading = false;
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
        title: Text('Audio Waveform Generator'),
      ),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextField(
              controller: _titleController,
              decoration: InputDecoration(
                labelText: 'Audio Title',
                border: OutlineInputBorder(),
              ),
            ),
            SizedBox(height: 16),
            ElevatedButton.icon(
              onPressed: _pickAudioFile,
              icon: Icon(Icons.audio_file),
              label: Text(_audioFile == null ? 'Select Audio File' : 'File Selected'),
            ),
            if (_audioFile != null) ...[
              SizedBox(height: 8),
              Text('Selected: ${_audioFile!.path.split('/').last}'),
            ],
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: _isUploading ? null : _uploadAudio,
              child: _isUploading 
                ? CircularProgressIndicator()
                : Text('Upload & Generate Waveform'),
            ),
            if (_uploadResult != null) ...[
              SizedBox(height: 24),
              Text('Upload Result:', style: Theme.of(context).textTheme.headline6),
              SizedBox(height: 8),
              Text('Title: ${_uploadResult!['title']}'),
              Text('ID: ${_uploadResult!['id']}'),
              SizedBox(height: 16),
              Text('Waveform Code:', style: Theme.of(context).textTheme.headline6),
              SizedBox(height: 8),
              WaveformDisplay(
                waveformUrl: _uploadResult!['code_image'],
                width: 300,
                height: 75,
              ),
            ],
          ],
        ),
      ),
    );
  }
}
```

## 🧪 Testing

### Test Waveform Generation

```bash
# Test the waveform generator
python test_waveform_generation.py

# Test with Django (if integrated)
python manage.py test_waveform
```

### Test API Endpoints

```bash
# Upload audio file
curl -X POST http://localhost:8000/api/audio/ \
  -F "title=Test Audio" \
  -F "audio_file=@test_audio.mp3"

# Get audio details
curl http://localhost:8000/api/audio/{id}/

# Regenerate waveform
curl -X POST http://localhost:8000/api/audio/{id}/regenerate_waveform/
```

## 🎨 Customization

### Waveform Appearance

```python
# Customize waveform appearance
generator = SpotifyWaveformGenerator(
    width=800,        # Image width
    height=200,       # Image height  
    bar_width=2,      # Bar thickness
    bar_spacing=1     # Space between bars
)
```

### Real Audio Analysis

For actual audio analysis instead of simulated waveforms:

```bash
pip install librosa
```

Then use `RealAudioWaveformGenerator` in your views.

## 🔧 Troubleshooting

### Common Issues

1. **Supabase Upload Fails**
   - Check bucket permissions
   - Verify credentials
   - Ensure bucket exists

2. **Cloudinary Upload Fails**
   - Verify API credentials
   - Check file size limits

3. **Waveform Not Reproducible**
   - Ensure using same audio ID as seed
   - Check UUID generation

4. **Flutter Network Errors**
   - Add internet permission
   - Check CORS settings
   - Verify API endpoints

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
    },
    'loggers': {
        'django_audio_waveform': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 📊 API Reference

### Endpoints

- `POST /api/audio/` - Upload audio and generate waveform
- `GET /api/audio/` - List all audio files
- `GET /api/audio/{id}/` - Get audio details
- `POST /api/audio/{id}/regenerate_waveform/` - Regenerate waveform
- `GET /api/audio/{id}/waveform_image/` - Get waveform image URL

### Response Format

```json
{
    "id": "uuid",
    "title": "Audio Title",
    "audio_file": "/media/audio_files/file.mp3",
    "code_image": "https://supabase.co/storage/wave_codes/waveform.png",
    "cloudinary_audio_url": "https://cloudinary.com/audio.mp3",
    "created_at": "2023-12-01T10:00:00Z",
    "updated_at": "2023-12-01T10:00:00Z"
}
```

## 🎉 Success!

Your Django + Supabase backend is now ready for your Flutter mobile app! 

- ✅ Audio files are uploaded and stored
- ✅ Spotify-style waveform codes are generated
- ✅ Images are uploaded to Supabase Storage
- ✅ Audio files are uploaded to Cloudinary
- ✅ Everything is linked in your database
- ✅ Flutter app can display the waveforms

The waveform patterns are reproducible - the same audio ID will always generate the same waveform code, just like Spotify!
