# 📱 Mobile App Usage Guide

## 🎵 Audio Art Frame Mobile App with Spotify Waveform Scanning

This guide will help you set up and use the Flutter mobile app to scan Spotify waveform codes and play audio messages.

## 🚀 Quick Start

### 1. **Start the API Server**
```bash
cd /home/badran/Downloads/Freelance_2025/audio_frame_art
python3 working_audio_api.py
```
The API will run on `http://localhost:8003`

### 2. **Run the Mobile App**

#### Option A: Flutter Web (Easiest)
```bash
cd mobile
flutter run -d web-server --web-port 8080 --web-hostname 0.0.0.0
```
Then open: `http://localhost:8080` in your browser

#### Option B: Android Device/Emulator
```bash
cd mobile
flutter run -d android
```

#### Option C: iOS Simulator (Mac only)
```bash
cd mobile
flutter run -d ios
```

## 📱 How to Use the Mobile App

### **Main Features:**

1. **🎯 QR Code Scanner**
   - Point your camera at any QR code
   - The app will automatically detect and process it
   - Works with both QR codes and Spotify waveform codes

2. **🎵 Audio Player**
   - Automatically plays audio when a valid code is scanned
   - Full playback controls (play, pause, stop, restart)
   - Progress bar and time display
   - Play count tracking

3. **📚 Scan History**
   - View all previously scanned frames
   - Track play counts for each frame
   - Quick access to previously played audio

### **Step-by-Step Usage:**

#### **Step 1: Grant Permissions**
- When you first open the app, it will ask for camera permission
- Tap "Grant Permission" to allow camera access
- This is required for scanning QR codes

#### **Step 2: Scan a Code**
- Point your camera at a QR code or Spotify waveform code
- The app will automatically detect and process it
- If successful, you'll be taken to the audio player screen

#### **Step 3: Play Audio**
- The audio will start playing automatically
- Use the controls to play, pause, stop, or restart
- The progress bar shows playback position
- Play count is tracked automatically

#### **Step 4: View History**
- Tap the history icon in the top-right corner
- View all previously scanned frames
- See play counts and scan times

## 🔧 Configuration

### **API Endpoint**
The app is configured to connect to: `http://localhost:8003/api`

If you need to change this, edit:
```dart
// mobile/lib/services/api_service.dart
static const String baseUrl = 'http://localhost:8003/api';
```

### **Network Access**
For mobile devices to connect to your computer:

1. **Find your computer's IP address:**
   ```bash
   ip addr show | grep inet
   ```

2. **Update the API URL in the mobile app:**
   ```dart
   static const String baseUrl = 'http://YOUR_IP_ADDRESS:8003/api';
   ```

3. **Make sure your firewall allows port 8003**

## 🎨 App Features

### **QR Code Scanning**
- **Supports:** QR codes, Spotify waveform codes
- **Format:** `audio_frame://frame/{frame_id}`
- **Auto-detection:** Automatically processes valid codes

### **Audio Playback**
- **Formats:** MP3, WAV, WebM, OGG
- **Controls:** Play, Pause, Stop, Restart, Seek
- **Progress:** Real-time progress bar and time display
- **Quality:** High-quality audio playback

### **History & Tracking**
- **Scan History:** All scanned frames with timestamps
- **Play Counts:** Local tracking of play counts
- **Offline Storage:** Data persists between app sessions

## 🐛 Troubleshooting

### **Common Issues:**

1. **"Camera permission required"**
   - Go to device settings and enable camera permission for the app
   - Or tap "Grant Permission" in the app

2. **"Error scanning frame"**
   - Check that the API server is running on port 8003
   - Verify the QR code is valid
   - Check network connection

3. **"Error playing audio"**
   - Check that the audio file exists and is accessible
   - Verify the audio URL is correct
   - Try restarting the app

4. **App won't start**
   - Run `flutter clean` and `flutter pub get`
   - Check that Flutter is properly installed
   - Try running on a different platform (web vs mobile)

### **Debug Mode:**
```bash
flutter run --debug
```
This will show detailed error messages in the console.

## 🔄 Testing the Complete Flow

### **1. Create an Order with Audio**
```bash
curl -X POST http://localhost:8003/api/orders/ \
  -F "customer_name=Test User" \
  -F "customer_phone=1234567890" \
  -F "customer_email=test@example.com" \
  -F "delivery_address=123 Test St" \
  -F "city=Test City" \
  -F "postal_code=12345" \
  -F "frame_id=1" \
  -F "payment_method=cash" \
  -F "total_amount=29.99" \
  -F "notes=Test order" \
  -F "audio_file=@test_audio.wav"
```

### **2. Get the Generated Waveform URL**
```bash
curl -X GET http://localhost:8003/api/orders/
```

### **3. Test Scanning**
- Use the mobile app to scan the generated waveform
- The app should detect it and play the audio

## 📊 API Endpoints Used by Mobile App

- `GET /api/frames/` - List available frames
- `GET /api/frames/{id}/` - Get specific frame details
- `GET /api/scan/{id}/` - Scan frame and get audio URL
- `POST /api/track-play/{id}/` - Track audio play event

## 🎯 Next Steps

1. **Test the complete flow** with real audio files
2. **Customize the UI** to match your brand
3. **Add more features** like sharing, favorites, etc.
4. **Deploy to app stores** when ready

## 📞 Support

If you encounter any issues:
1. Check the API server logs
2. Check the Flutter console output
3. Verify network connectivity
4. Test with different audio files

---

**Happy scanning! 🎵📱**
