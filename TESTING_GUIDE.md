# 🧪 Complete Testing Guide for Audio Frame Art

## 🌐 **Testing the Website**

### **Step 1: Access the Website**
Open your web browser and go to:
- **Main Website**: http://localhost:3000
- **Frames Page**: http://localhost:3000/frames

### **Step 2: Test the Complete Order Flow**

#### **2.1 Browse Frames**
1. Go to http://localhost:3000/frames
2. You should see 6 frames displayed in Arabic
3. Each frame shows:
   - Title in Arabic
   - Description in Arabic
   - Price in Algerian Dinars (DZD)
   - Frame type (wooden, metal, glass, plastic)
   - "Available" status

#### **2.2 Select a Frame**
1. Click on any frame's "View Details" or "Order Frame" button
2. You should be redirected to the order page
3. The order page should show:
   - Frame information
   - Order form in Arabic
   - Audio recording section

#### **2.3 Fill Order Form**
1. **Customer Name**: Enter your name
2. **Phone Number**: Enter a 10-digit number (e.g., 0555123456)
3. **Wilaya**: Select from dropdown (e.g., الجزائر)
4. **Baladya**: Enter city name (e.g., الجزائر)
5. **Address**: Enter detailed address
6. **Audio Message**: 
   - Click the microphone to record
   - OR click "Upload Audio File" to select a file
7. **Terms**: Check the terms and conditions checkbox

#### **2.4 Submit Order**
1. Click "Create Order" button
2. You should see a success page
3. The order should be created successfully

### **Step 3: Test API Endpoints**

#### **3.1 Test Frames API**
```bash
curl http://localhost:8001/api/frames/
```
Should return a list of 6 frames in JSON format.

#### **3.2 Test Order Creation**
```bash
curl -X POST http://localhost:8001/api/orders/ \
  -F "customer_name=Test User" \
  -F "customer_phone=0555123456" \
  -F "delivery_address=Test Address" \
  -F "city=Algiers" \
  -F "wilaya=الجزائر" \
  -F "baladya=الجزائر" \
  -F "frame=1" \
  -F "payment_method=COD"
```
Should return a success response with order details.

#### **3.3 Test QR Code Scanning**
```bash
curl http://localhost:8001/api/scan/1/
```
Should return frame information and audio URL.

## 📱 **Testing the Mobile App**

### **Step 1: Start the Mobile App**

#### **Option A: Web Version (Easiest)**
```bash
cd /home/badran/Downloads/Freelance_2025/audio_frame_art/mobile
flutter run -d web-server --web-port 8081
```
Then open: http://localhost:8081

#### **Option B: Android Emulator**
```bash
cd /home/badran/Downloads/Freelance_2025/audio_frame_art/mobile
flutter run
```

#### **Option C: Physical Device**
1. Connect your phone via USB
2. Enable USB debugging
3. Run: `flutter run`

### **Step 2: Test QR Code Scanning**

#### **2.1 Create a Test QR Code**
1. Go to http://localhost:8001/api/scan/1/
2. Copy the response
3. Create a QR code with this URL: `http://localhost:8001/api/scan/1/`
4. You can use any QR code generator online

#### **2.2 Test Scanning in Mobile App**
1. Open the mobile app
2. Grant camera permission when prompted
3. Point camera at the QR code
4. The app should:
   - Detect the QR code
   - Navigate to audio player screen
   - Show frame information
   - Display audio player controls

#### **2.3 Test Audio Playback**
1. On the audio player screen
2. Click the play button
3. Audio should start playing (if available)
4. You should see:
   - Play/pause controls
   - Progress bar
   - Play count
   - Frame information

### **Step 3: Test Mobile App Features**

#### **3.1 Scan History**
1. Scan multiple QR codes
2. Go to History tab
3. You should see list of scanned frames
4. Each entry should show:
   - Frame title
   - Scan time
   - Frame ID

#### **3.2 Audio Controls**
1. Play audio
2. Test pause/resume
3. Test stop button
4. Test seek functionality
5. Test restart button

## 🔧 **Troubleshooting**

### **Common Issues and Solutions**

#### **Website Not Loading**
```bash
# Check if containers are running
docker-compose ps

# Restart if needed
docker-compose restart

# Check logs
docker-compose logs web
```

#### **API Not Responding**
```bash
# Check API health
curl http://localhost:8001/health/

# Check API logs
docker-compose logs api

# Restart API
docker-compose restart api
```

#### **Mobile App Not Starting**
```bash
# Check Flutter doctor
flutter doctor

# Clean and rebuild
flutter clean
flutter pub get
flutter run
```

#### **QR Code Not Scanning**
1. Ensure camera permission is granted
2. Check if QR code is valid
3. Try with different lighting
4. Make sure QR code contains the correct URL

#### **Audio Not Playing**
1. Check if audio file exists
2. Check browser/device audio settings
3. Try different audio formats
4. Check network connection

## 📊 **Testing Checklist**

### **Website Testing**
- [ ] Homepage loads correctly
- [ ] Frames page displays all frames
- [ ] Order form works
- [ ] Audio recording works
- [ ] Order submission succeeds
- [ ] Success page shows
- [ ] Arabic text displays correctly
- [ ] RTL layout works

### **API Testing**
- [ ] Health check passes
- [ ] Frames API returns data
- [ ] Order creation works
- [ ] QR scan returns audio URL
- [ ] Statistics API works
- [ ] File upload works

### **Mobile App Testing**
- [ ] App starts successfully
- [ ] Camera permission granted
- [ ] QR code scanning works
- [ ] Audio player loads
- [ ] Audio playback works
- [ ] Controls function properly
- [ ] History saves scans
- [ ] Play tracking works

## 🚀 **Quick Test Commands**

### **Run All Tests**
```bash
cd /home/badran/Downloads/Freelance_2025/audio_frame_art
python3 test_complete_flow.py
```

### **Test Website Only**
```bash
curl -s http://localhost:3000 | grep -o "<title>.*</title>"
```

### **Test API Only**
```bash
curl http://localhost:8001/health/
```

### **Test Mobile App**
```bash
cd mobile
flutter run -d web-server --web-port 8081
```

## 📱 **Mobile App URLs**

- **Web Version**: http://localhost:8081
- **QR Code Test**: http://localhost:8001/api/scan/1/
- **API Health**: http://localhost:8001/health/

## 🎯 **Expected Results**

### **Website**
- Beautiful Arabic interface
- 6 frames displayed
- Order form works
- Audio recording/upload works
- Orders created successfully

### **Mobile App**
- QR scanner interface
- Audio player with controls
- Scan history
- Play tracking
- Smooth user experience

### **API**
- All endpoints respond correctly
- Orders are created and stored
- QR scans return audio URLs
- Statistics are tracked
- File uploads work

---

## 🎉 **Success Indicators**

You'll know everything is working when:
- ✅ Website loads with Arabic content
- ✅ Orders can be placed successfully
- ✅ Mobile app scans QR codes
- ✅ Audio plays in mobile app
- ✅ All API endpoints respond
- ✅ Statistics are tracked

**Your Audio Frame Art system is ready for business!** 🚀