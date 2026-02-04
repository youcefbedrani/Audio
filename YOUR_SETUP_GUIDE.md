# 🚀 Your Audio Art Frame Setup Guide

## ✅ What You Have
- **Cloudinary Cloud Name**: `dulct8pma`
- **Cloudinary URL Format**: `cloudinary://<your_api_key>:<your_api_secret>@dulct8pma`

## 🔧 What You Need To Do

### Step 1: Get Your Cloudinary API Key and Secret

1. Go to [Cloudinary Console](https://cloudinary.com/console)
2. Login to your account
3. Copy your **API Key** and **API Secret** from the dashboard
4. Replace `<your_api_key>` and `<your_api_secret>` in the URL below

### Step 2: Update Your .env File

Edit the `.env` file in your project root and update these lines:

```bash
# Cloudinary Configuration
CLOUDINARY_URL=cloudinary://YOUR_ACTUAL_API_KEY:YOUR_ACTUAL_API_SECRET@dulct8pma
CLOUDINARY_CLOUD_NAME=dulct8pma
CLOUDINARY_API_KEY=YOUR_ACTUAL_API_KEY
CLOUDINARY_API_SECRET=YOUR_ACTUAL_API_SECRET

# Frontend Configuration
NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME=dulct8pma
```

**Example** (replace with your actual values):
```bash
CLOUDINARY_URL=cloudinary://123456789012345:abcdefghijklmnopqrstuvwxyz123456@dulct8pma
CLOUDINARY_CLOUD_NAME=dulct8pma
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=abcdefghijklmnopqrstuvwxyz123456
NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME=dulct8pma
```

### Step 3: Install Docker Compose (if not installed)

```bash
# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

### Step 4: Run the Project

```bash
# Start all services
docker-compose -f docker-compose.dev.yml up --build

# In another terminal, setup the database
docker-compose -f docker-compose.dev.yml exec api python manage.py migrate

# Create admin user
docker-compose -f docker-compose.dev.yml exec api python manage.py createsuperuser
```

### Step 5: Access Your Applications

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Admin Dashboard**: http://localhost:8000/admin

## 🧪 Test Your Setup

Run the test script to verify everything is working:

```bash
./test_setup.sh
```

## 📱 Complete User Flow

### 1. Admin Setup (First Time)
1. Go to http://localhost:8000/admin
2. Login with your superuser credentials
3. Create some sample frames with images
4. Add audio files to frames

### 2. Customer Flow
1. Go to http://localhost:3000
2. Browse available frames
3. Select a frame and record audio
4. Place an order with delivery details
5. Get QR code for the frame

### 3. Mobile App Flow
1. Install the Flutter app on your device
2. Scan the QR code from the frame
3. Listen to the audio message
4. View scan history

## 🔍 Troubleshooting

### If Backend Fails to Start
```bash
# Check Cloudinary configuration
docker-compose -f docker-compose.dev.yml logs api

# Common issues:
# 1. Wrong API key/secret
# 2. Cloudinary URL format incorrect
# 3. Network connectivity issues
```

### If Frontend Shows Errors
```bash
# Check if backend is running
curl http://localhost:8000/api/frames/

# Should return JSON response
```

### If Mobile App Can't Connect
```bash
# Update mobile API URL in:
# mobile/lib/services/api_service.dart
# Change baseUrl to your actual backend URL
```

## 🎯 What You Can Do Right Now

1. **Create Frames**: Add art frames with images
2. **Record Audio**: Use browser microphone to record messages
3. **Process Orders**: Handle customer orders with delivery details
4. **Generate QR Codes**: Automatic QR code generation for frames
5. **Scan & Play**: Mobile app scans QR codes and plays audio
6. **Track Analytics**: Monitor scans, plays, and orders
7. **Manage Business**: Admin dashboard for complete control

## 🚀 Production Deployment

When ready for production:

```bash
# Update .env with production values
# Set DEBUG=False
# Add your domain to ALLOWED_HOSTS
# Run production deployment
./deploy.sh
```

## 📞 Need Help?

If you encounter any issues:

1. **Check logs**: `docker-compose -f docker-compose.dev.yml logs`
2. **Verify Cloudinary**: Make sure your API key/secret are correct
3. **Test connectivity**: Ensure ports 3000, 8000, 5432 are free
4. **Run test script**: `./test_setup.sh` for automated diagnostics

## 🎉 Success!

Once everything is running, you'll have:
- ✅ Complete web application for customers
- ✅ Mobile app for QR code scanning
- ✅ Admin dashboard for business management
- ✅ Automatic QR code generation
- ✅ Audio recording and playback
- ✅ Order processing system
- ✅ Analytics and tracking

**Your Audio Art Frame business is ready to go!** 🚀
