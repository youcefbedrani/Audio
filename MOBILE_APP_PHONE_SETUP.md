# 📱 Mobile App - Phone Setup Guide

## ✅ APK Built Successfully!

**APK Location:** `mobile/build/app/outputs/flutter-apk/app-debug.apk`  
**Size:** ~103 MB  
**API URL:** `http://192.168.1.18:8001/api` (Your computer's IP)

---

## 📲 Installation Methods

### **Method 1: Direct USB Install (Recommended - Fastest)**

1. **Connect your phone via USB cable**

2. **Enable USB Debugging on your phone:**
   - Go to **Settings** > **About Phone**
   - Tap **Build Number** 7 times (you'll see "You are now a developer!")
   - Go back to **Settings** > **Developer Options**
   - Enable **USB Debugging**
   - Allow the computer when prompted on phone

3. **Install via ADB:**
   ```bash
   cd /home/badran/Downloads/Freelance_2025/audio_frame_art/mobile
   adb install build/app/outputs/flutter-apk/app-debug.apk
   ```

   Or use Flutter:
   ```bash
   cd mobile
   flutter install
   ```

---

### **Method 2: Transfer APK Manually (No USB)**

1. **Transfer APK to phone:**
   - **Google Drive:** Upload APK to Google Drive, download on phone
   - **Email:** Email the APK to yourself, open on phone
   - **Bluetooth:** Send APK via Bluetooth from computer to phone
   - **USB Mass Storage:** Connect phone as storage device, copy APK

2. **On your phone:**
   - Open **File Manager**
   - Navigate to downloaded APK file
   - Tap on `app-debug.apk`
   - Allow **"Install from unknown sources"** if prompted
   - Tap **"Install"**

---

## ⚙️ Before Using the App

### **1. Start API Server:**
```bash
cd /home/badran/Downloads/Freelance_2025/audio_frame_art
python3 supabase_docker_api.py
```
API should run on `http://0.0.0.0:8001`

### **2. Verify Network Connection:**
- **Phone and computer must be on the SAME WiFi network**
- Check your computer's IP: `hostname -I` (should show `192.168.1.18`)
- Test API accessibility from phone browser:
  ```
  http://192.168.1.18:8001/api/frames/
  ```
  Should show JSON with frames list

### **3. Firewall Settings:**
- Make sure firewall allows port 8001
- On Linux:
  ```bash
  sudo ufw allow 8001/tcp
  ```

---

## 🎯 How to Use the App

### **Step 1: Grant Permissions**
- Open the app
- When prompted, **allow camera permission**
- This is required for scanning waveform codes

### **Step 2: Scan a Waveform Code**
- Point camera at a Spotify waveform code (from an order)
- App will automatically detect and process it
- If successful, audio player screen will open

### **Step 3: Play Audio**
- Audio will start playing automatically
- Use controls to play, pause, stop, or restart
- Progress bar shows playback position
- Play count is tracked automatically

### **Step 4: View History**
- Tap history icon (top-right)
- View all previously scanned frames
- See play counts and scan times

---

## 🔧 Troubleshooting

### **"Can't connect to API"**
- Check API server is running: `curl http://192.168.1.18:8001/api/frames/`
- Verify phone and computer are on same WiFi
- Check firewall allows port 8001

### **"Camera permission denied"**
- Go to phone Settings > Apps > Audio Art Frame > Permissions
- Enable Camera permission

### **"Audio won't play"**
- Check internet connection
- Verify audio URL is accessible
- Check device volume

### **"App crashes"**
- Restart the app
- Check phone has enough storage (need ~150MB)
- Reinstall the APK

---

## 📝 API Configuration

The app is currently configured to connect to:
```
http://192.168.1.18:8001/api
```

**To change this:**
1. Edit `mobile/lib/services/api_service.dart`
2. Change `baseUrl` to your desired IP/port
3. Rebuild APK: `flutter build apk --debug`

---

## ✅ Quick Test

1. **Create an order** with audio on your website
2. **Get the waveform code** (displayed on order confirmation)
3. **Open mobile app** on your phone
4. **Scan the waveform code** with camera
5. **Listen to the audio message**!

---

**🎉 Your mobile app is ready! Enjoy scanning and listening to audio messages!**

