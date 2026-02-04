# Audio Art Frame - Complete Setup Guide

This guide will help you set up the entire Audio Art Frame system with all necessary configurations.

## 🔧 Environment Configuration

### 1. Create .env File

Copy the example file and configure it:

```bash
cp env.example .env
```

### 2. Complete .env Configuration

Here's what you need to configure in your `.env` file:

```bash
# ===========================================
# DJANGO SETTINGS
# ===========================================
SECRET_KEY=your-super-secret-key-here-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,yourdomain.com

# ===========================================
# DATABASE CONFIGURATION
# ===========================================
DB_NAME=audio_frame_db
DB_USER=postgres
DB_PASSWORD=your-secure-database-password
DB_HOST=db
DB_PORT=5432

# ===========================================
# CLOUDINARY CONFIGURATION (REQUIRED)
# ===========================================
# Get these from https://cloudinary.com/console
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# ===========================================
# JWT AUTHENTICATION
# ===========================================
JWT_SECRET_KEY=your-jwt-secret-key-different-from-secret-key

# ===========================================
# FRONTEND CONFIGURATION
# ===========================================
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME=your-cloud-name

# ===========================================
# MOBILE APP CONFIGURATION
# ===========================================
MOBILE_API_URL=http://localhost:8000
```

## 🌩️ Cloudinary Setup (CRITICAL)

### Step 1: Create Cloudinary Account

1. Go to [https://cloudinary.com](https://cloudinary.com)
2. Sign up for a free account
3. Verify your email

### Step 2: Get Your Credentials

1. Go to [Cloudinary Console](https://cloudinary.com/console)
2. Copy your credentials from the dashboard:

```
Cloud Name: abc123def456
API Key: 123456789012345
API Secret: abcdefghijklmnopqrstuvwxyz123456
```

### Step 3: Update .env File

Replace the Cloudinary values in your `.env`:

```bash
CLOUDINARY_CLOUD_NAME=abc123def456
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=abcdefghijklmnopqrstuvwxyz123456
NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME=abc123def456
```

### Step 4: Test Cloudinary Connection

We'll test this in the backend setup.

## 🐳 Docker Setup

### Prerequisites

Make sure you have Docker and Docker Compose installed:

```bash
# Check if Docker is installed
docker --version
docker-compose --version

# If not installed, install Docker:
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## 🚀 Quick Start Commands

### Development Mode

```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up --build

# In another terminal, run migrations
docker-compose -f docker-compose.dev.yml exec api python manage.py migrate

# Create admin user
docker-compose -f docker-compose.dev.yml exec api python manage.py createsuperuser
```

### Production Mode

```bash
# Deploy with the deployment script
./deploy.sh
```

## 📱 Testing Each Component

Let's test each component to ensure everything works:

### 1. Backend API Testing

```bash
# Test API endpoints
curl http://localhost:8000/api/frames/
curl http://localhost:8000/api/health/
```

### 2. Frontend Testing

```bash
# Access the web application
open http://localhost:3000
```

### 3. Mobile App Testing

```bash
# Run Flutter app
cd mobile
flutter run
```

## 🔍 Troubleshooting

### Common Issues

1. **Cloudinary Connection Failed**
   - Check your credentials in .env
   - Verify Cloudinary account is active
   - Check internet connection

2. **Database Connection Issues**
   - Ensure PostgreSQL is running
   - Check database credentials
   - Verify Docker containers are up

3. **Port Conflicts**
   - Check if ports 3000, 8000, 5432 are free
   - Use `lsof -i :PORT` to check port usage

4. **Permission Issues**
   - Make sure deploy.sh is executable: `chmod +x deploy.sh`
   - Check Docker permissions

## 📊 Monitoring

### Check Service Status

```bash
# Check all containers
docker-compose ps

# View logs
docker-compose logs -f

# Check specific service logs
docker-compose logs -f api
docker-compose logs -f web
docker-compose logs -f db
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health/

# Frontend health
curl http://localhost:3000/

# Database health
docker-compose exec db pg_isready -U postgres
```

## 🎯 Next Steps

1. **Configure Cloudinary** (Required)
2. **Set up your domain** (For production)
3. **Create SSL certificates** (For production)
4. **Set up monitoring** (Optional)
5. **Configure backups** (Recommended)

## 📞 Support

If you encounter any issues:

1. Check the logs: `docker-compose logs`
2. Verify your .env configuration
3. Ensure all services are running: `docker-compose ps`
4. Check the troubleshooting section above
