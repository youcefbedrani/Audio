# 📱 Mobile App Installation Guide

## ✅ **APK Successfully Built!**

Your Audio Frame Art mobile app has been successfully built as an Android APK file.

### 📁 **APK Location:**
```
/home/badran/Downloads/Freelance_2025/audio_frame_art/mobile/build/app/outputs/flutter-apk/app-debug.apk
```

**File Size:** ~107 MB  
**Type:** Debug APK (easier to install and test)

---

## 📲 **How to Install on Your Android Phone:**

### **Method 1: Direct Transfer (Recommended)**

1. **Copy APK to your phone:**
   ```bash
   # Copy to a USB drive or cloud storage
   cp /home/badran/Downloads/Freelance_2025/audio_frame_art/mobile/build/app/outputs/flutter-apk/app-debug.apk /path/to/usb/drive/
   ```

2. **Transfer to your phone:**
   - Connect USB drive to your phone, OR
   - Upload to Google Drive/Dropbox and download on phone, OR
   - Email the APK to yourself

3. **Install on phone:**
   - Open file manager on your phone
   - Navigate to the APK file
   - Tap on `app-debug.apk`
   - Allow installation from unknown sources when prompted
   - Tap "Install"

### **Method 2: ADB Installation (If you have ADB setup)**

1. **Enable Developer Options on your phone:**
   - Go to Settings > About Phone
   - Tap "Build Number" 7 times
   - Go back to Settings > Developer Options
   - Enable "USB Debugging"

2. **Install via ADB:**
   ```bash
   adb install /home/badran/Downloads/Freelance_2025/audio_frame_art/mobile/build/app/outputs/flutter-apk/app-debug.apk
   ```

---

## 🎯 **App Features:**

### **📷 QR Code Scanner**
- Point camera at any QR code or Spotify waveform code
- Automatically detects and processes codes
- Works with both QR codes and Spotify-style waveform codes

### **🎵 Audio Player**
- Play audio messages with full controls
- Play, pause, stop, restart functionality
- Volume control and progress tracking

### **📊 History & Analytics**
- View all scanned frames
- Track play counts for each audio
- Local storage of scan history

### **🔧 Settings**
- Camera permission management
- Audio playback preferences
- Clear history option

---

## 🌐 **API Configuration:**

The app is configured to connect to your API server at:
- **API URL:** `http://localhost:8003/api` (for local testing)
- **Server:** Your Flask API with Spotify waveform generation

### **For Network Access (Other devices):**

If you want to use the app from other devices on your network:

1. **Find your computer's IP address:**
   ```bash
   hostname -I
   ```

2. **Update the API URL in the app:**
   - Edit `mobile/lib/services/api_service.dart`
   - Change `baseUrl` to `http://YOUR_IP:8003/api`

3. **Rebuild the APK:**
   ```bash
   cd /home/badran/Downloads/Freelance_2025/audio_frame_art/mobile
   flutter build apk --debug
   ```

---

## 🧪 **Testing the Complete Flow:**

### **1. Start Your API Server:**
```bash
cd /home/badran/Downloads/Freelance_2025/audio_frame_art
python3 working_audio_api.py
```

### **2. Create a Test Order:**
- Go to your web frontend
- Create an order with audio upload
- The API will generate a Spotify waveform code

### **3. Test with Mobile App:**
- Open the installed mobile app
- Grant camera permission
- Scan the generated waveform code
- Listen to the audio message

---

## 🔧 **Troubleshooting:**

### **Installation Issues:**
- **"Installation blocked"**: Enable "Install from unknown sources" in Android settings
- **"App not installed"**: Check if you have enough storage space (need ~150MB)
- **"Package appears to be corrupt"**: Re-download the APK file

### **App Issues:**
- **Camera not working**: Grant camera permission in app settings
- **Audio not playing**: Check if your API server is running on port 8003
- **Can't connect to API**: Verify the API URL in the app configuration

### **API Connection Issues:**
- **"Connection refused"**: Make sure your Flask API is running
- **"Network error"**: Check if your phone and computer are on the same network

---

## 📱 **App Permissions Required:**

- **Camera**: To scan QR codes and waveform codes
- **Storage**: To save scan history and audio files
- **Internet**: To connect to your API server
- **Audio**: To play audio messages

---

## 🎉 **Success!**

Your mobile app is now ready to:
1. **Scan Spotify waveform codes** from your audio frame orders
2. **Play audio messages** with full player controls
3. **Track scan history** and play statistics
4. **Work offline** for previously scanned codes

The app will automatically connect to your API server and provide a seamless experience for your customers to listen to their personalized audio messages!

---

## 📞 **Support:**

If you encounter any issues:
1. Check that your API server is running on port 8003
2. Verify the API URL in the app configuration
3. Ensure your phone has the required permissions
4. Check the network connection between your phone and computer

**Happy scanning! 🎵📱**
