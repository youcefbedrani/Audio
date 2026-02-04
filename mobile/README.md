# Audio Art Frame - Mobile App

Flutter mobile application for scanning QR codes and playing audio messages from Audio Art Frames.

## Features

- **QR Code Scanning**: Scan Audio Art Frame QR codes using device camera
- **Audio Playback**: Play audio messages with full player controls
- **Scan History**: View history of previously scanned frames
- **Offline Support**: Local storage for scan history and play counts
- **Modern UI**: Clean, intuitive interface with Material Design

## Setup

1. **Install Flutter**
   ```bash
   # Follow Flutter installation guide for your platform
   # https://docs.flutter.dev/get-started/install
   ```

2. **Install Dependencies**
   ```bash
   flutter pub get
   ```

3. **Configure API URL**
   Update the API base URL in `lib/services/api_service.dart`:
   ```dart
   static const String baseUrl = 'http://your-api-url.com/api';
   ```

4. **Run the App**
   ```bash
   flutter run
   ```

## Permissions

The app requires the following permissions:

- **Camera**: For QR code scanning
- **Internet**: For API communication
- **Storage**: For local data caching

## Architecture

### Models
- `Frame`: Represents an art frame with metadata
- `ScanResponse`: Response from scanning a QR code
- `PlayTrackResponse`: Response from tracking audio plays

### Services
- `ApiService`: Handles all API communication
- `AudioService`: Manages audio playback using just_audio

### Screens
- `HomeScreen`: Main scanning interface
- `AudioPlayerScreen`: Audio playback with controls
- `HistoryScreen`: View scan history

## API Integration

The app communicates with the Django backend API:

- `GET /api/scan/{frame_id}/` - Scan frame and get audio URL
- `POST /api/track-play/{frame_id}/` - Track audio play event

## Local Storage

Uses SharedPreferences for:
- Scan history (last 50 scans)
- Local play counts per frame
- User preferences

## QR Code Format

Expected QR code format:
```
audio_frame://frame/{frame_id}
```

## Building for Production

### Android
```bash
flutter build apk --release
```

### iOS
```bash
flutter build ios --release
```

## Troubleshooting

### Camera Permission Issues
- Ensure camera permission is granted in device settings
- For Android, check `android/app/src/main/AndroidManifest.xml`
- For iOS, check `ios/Runner/Info.plist`

### Audio Playback Issues
- Ensure device volume is up
- Check internet connection for audio streaming
- Verify audio URL is accessible

### API Connection Issues
- Verify API URL is correct and accessible
- Check network connectivity
- Ensure backend server is running

## Dependencies

- `mobile_scanner`: QR code scanning
- `just_audio`: Audio playback
- `http`: API communication
- `shared_preferences`: Local storage
- `permission_handler`: Permission management