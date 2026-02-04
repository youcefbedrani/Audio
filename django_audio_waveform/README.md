# Django Audio Waveform Generator

A Django app that generates Spotify-style waveform code images from audio files and uploads them to Supabase Storage.

## Features

- 🎵 **Audio File Upload**: Handle MP3/WAV file uploads
- 📊 **Waveform Generation**: Create reproducible Spotify-style waveform codes
- ☁️ **Cloud Storage**: Upload audio to Cloudinary and waveforms to Supabase Storage
- 🔄 **Reproducible**: Same audio ID always generates the same waveform pattern
- 🎨 **Customizable**: Configurable dimensions, bar width, and spacing

## Installation

1. **Install the package**:
```bash
pip install -r requirements.txt
```

2. **Add to Django settings**:
```python
INSTALLED_APPS = [
    # ... other apps
    'rest_framework',
    'django_audio_waveform',
]

# Add Supabase and Cloudinary configuration
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your-anon-key"
CLOUDINARY_CLOUD_NAME = "your-cloud-name"
CLOUDINARY_API_KEY = "your-api-key"
CLOUDINARY_API_SECRET = "your-api-secret"
```

3. **Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Create Supabase Storage bucket**:
   - Go to your Supabase dashboard
   - Create a storage bucket named `wave_codes`
   - Set it to public

## Usage

### API Endpoints

#### Upload Audio File
```http
POST /api/audio/
Content-Type: multipart/form-data

{
    "title": "My Audio Track",
    "audio_file": <file>
}
```

**Response**:
```json
{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "My Audio Track",
    "audio_file": "/media/audio_files/audio.mp3",
    "code_image": "https://your-project.supabase.co/storage/v1/object/public/wave_codes/waveform_123e4567.png",
    "cloudinary_audio_url": "https://res.cloudinary.com/your-cloud/video/upload/v1234567890/audio.mp3",
    "created_at": "2023-12-01T10:00:00Z",
    "updated_at": "2023-12-01T10:00:00Z"
}
```

#### Regenerate Waveform
```http
POST /api/audio/{id}/regenerate_waveform/
```

#### Get Waveform Image URL
```http
GET /api/audio/{id}/waveform_image/
```

### Python Usage

```python
from django_audio_waveform.waveform_generator import SpotifyWaveformGenerator

# Create generator
generator = SpotifyWaveformGenerator(width=800, height=200)

# Generate waveform from audio file
waveform_bytes = generator.generate_waveform_bytes(
    audio_file_path="path/to/audio.mp3",
    audio_id="unique-audio-id"
)

# Save to file
with open("waveform.png", "wb") as f:
    f.write(waveform_bytes)
```

## Configuration

### Waveform Generator Settings

```python
generator = SpotifyWaveformGenerator(
    width=800,        # Image width in pixels
    height=200,       # Image height in pixels
    bar_width=2,      # Width of each bar
    bar_spacing=1     # Space between bars
)
```

### Real Audio Analysis (Optional)

For actual audio analysis instead of simulated waveforms:

```bash
pip install librosa
```

Then use `RealAudioWaveformGenerator`:

```python
from django_audio_waveform.waveform_generator import RealAudioWaveformGenerator

generator = RealAudioWaveformGenerator()
```

## Testing

Test waveform generation:

```bash
python manage.py test_waveform
```

Test specific audio:

```bash
python manage.py test_waveform --audio-id 123e4567-e89b-12d3-a456-426614174000
```

## Flutter Integration

### Upload Audio File

```dart
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';

Future<Map<String, dynamic>> uploadAudio(String title, File audioFile) async {
  var request = http.MultipartRequest(
    'POST',
    Uri.parse('https://your-api.com/api/audio/'),
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
  
  return json.decode(responseData);
}
```

### Display Waveform

```dart
import 'package:flutter/material.dart';

class WaveformDisplay extends StatelessWidget {
  final String waveformUrl;
  
  const WaveformDisplay({Key? key, required this.waveformUrl}) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return Image.network(
      waveformUrl,
      width: 800,
      height: 200,
      fit: BoxFit.cover,
    );
  }
}
```

## File Structure

```
django_audio_waveform/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── serializers.py
├── urls.py
├── views.py
├── waveform_generator.py
├── requirements.txt
├── settings_example.py
├── management/
│   └── commands/
│       └── test_waveform.py
└── README.md
```

## Troubleshooting

### Common Issues

1. **Supabase Upload Fails**: Check your Supabase credentials and bucket permissions
2. **Cloudinary Upload Fails**: Verify your Cloudinary configuration
3. **Waveform Not Reproducible**: Ensure you're using the same audio ID as seed
4. **Image Quality Issues**: Adjust `bar_width` and `bar_spacing` parameters

### Debug Mode

Enable debug logging in Django settings:

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

## License

MIT License - feel free to use in your projects!
