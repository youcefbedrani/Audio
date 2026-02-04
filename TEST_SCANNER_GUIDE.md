# 📱 Mobile App Scanner - Test Guide

## ❌ Why Your Old Waveform Codes Don't Work

### The Problem:
1. **Old waveform codes don't have visible QR codes**
   - They were generated before the QR code feature was added
   - The QR code was embedded in the waveform pattern (not visible)
   - Very hard for scanners to detect

2. **QR code was too small or hidden**
   - Embedded QR codes are covered by waveform bars
   - Scanner can't detect them reliably

3. **New waveform codes have LARGE visible QR code**
   - 180x180px+ QR code box on the RIGHT side
   - White background with black border
   - Easy to scan!

## ✅ Solution: Test Without Scanning

### Method 1: Use Test Button in App
1. Open the mobile app
2. Look for the **bug icon** (🐛) in the top-right corner
3. Tap it to open "Test Scanner" dialog
4. Click **"Test Scan Frame ID: 1"** button
5. This will:
   - Call API directly (no scanning needed)
   - Fetch audio from Supabase
   - Play audio from Cloudinary
   - Show if everything works!

### Method 2: Create New Order
1. Go to your web app
2. Create a **NEW order** with audio recording
3. The new waveform will have:
   - **LARGE QR code box** on the RIGHT side
   - Easy to scan with mobile app
   - Works like Spotify codes!

## 🧪 Testing Steps

### Step 1: Test Scanner Without QR Code
```
1. Open mobile app
2. Tap bug icon (🐛) in top-right
3. Click "Test Scan Frame ID: 1"
4. Wait for audio to play
5. If audio plays → Scanner works! ✅
6. If error → Check API/network
```

### Step 2: Check API is Working
```bash
curl http://192.168.1.18:8001/api/scan/1/
```
Should return JSON with `audio_url` from Cloudinary.

### Step 3: Create New Order (To Get Scannable QR)
```
1. Go to web app
2. Create order with frame ID 1
3. Record audio
4. Submit order
5. Download/view waveform
6. You'll see LARGE QR code on RIGHT side
7. Scan with mobile app
```

## 🔍 Troubleshooting

### If Test Button Works But Scanning Doesn't:
- **Problem**: Old waveform codes don't have visible QR
- **Solution**: Create NEW order to get scannable QR code

### If Test Button Fails:
- **Problem**: API not accessible or no audio for frame
- **Check**:
  1. API server running on `192.168.1.18:8001`?
  2. Phone and computer on same Wi-Fi?
  3. Order with audio exists for frame ID?

### If Scanner Doesn't Detect QR:
- **Problem**: QR code too small or hidden
- **Solution**: New waveform codes have LARGE visible QR (180x180px+)

## 📋 Quick Test Checklist

- [ ] Test button works? → Scanner is OK
- [ ] Test button fails? → Check API/network
- [ ] Can't scan old codes? → Normal! Create new order
- [ ] New code has visible QR? → Should work!
- [ ] Audio plays after scan? → Complete success! ✅

## 💡 Key Points

1. **Old codes = No visible QR = Can't scan** ❌
2. **New codes = Large visible QR = Easy to scan** ✅
3. **Test button = Skip scanning, test directly** ✅
4. **Always test with NEW orders** ✅

