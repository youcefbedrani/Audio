# 🐳 Docker Setup Guide

## Quick Start with Docker

### 1. Prerequisites
- Docker and Docker Compose installed
- Your Supabase database password

### 2. Setup Environment Variables

```bash
# Copy the environment template
cp env.example .env

# Edit .env file with your actual values
nano .env
```

**Required changes in .env:**
- `DB_PASSWORD=your-actual-supabase-db-password`
- `CLOUDINARY_API_KEY=your-cloudinary-api-key`
- `CLOUDINARY_API_SECRET=your-cloudinary-api-secret`
- `SECRET_KEY=your-django-secret-key`
- `JWT_SECRET_KEY=your-jwt-secret-key`

### 3. Start with Docker

```bash
# Option 1: Use the setup script
./setup-docker.sh

# Option 2: Manual Docker commands
docker-compose up --build -d
```

### 4. Access Your Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

### 5. Static HTML Pages (Alternative)

If you prefer static HTML pages:
- **Homepage**: http://localhost:3000/index.html
- **Frames List**: http://localhost:3000/frames.html
- **Frame Details**: http://localhost:3000/frame-detail.html?id=5
- **Thank You**: http://localhost:3000/thank-you.html

### 6. Useful Docker Commands

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Rebuild and start
docker-compose up --build -d

# Check service status
docker-compose ps
```

### 7. Troubleshooting

**If services don't start:**
```bash
# Check logs for errors
docker-compose logs api
docker-compose logs web

# Rebuild from scratch
docker-compose down
docker-compose up --build --force-recreate -d
```

**If database connection fails:**
- Verify your Supabase credentials in `.env`
- Make sure the database schema is created in Supabase
- Check that your IP is whitelisted in Supabase

### 8. Development vs Production

**Development (current setup):**
- Uses Supabase cloud database
- Frontend accessible at localhost:3000
- Backend accessible at localhost:8000

**Production:**
- Add SSL certificates
- Use production database
- Configure proper domain names
- Set DEBUG=False

## 🎯 What's Working

✅ **Docker Configuration**: Updated for Supabase
✅ **Frontend**: Next.js with static HTML alternatives
✅ **Backend**: Django with Supabase integration
✅ **Database**: Supabase cloud PostgreSQL
✅ **Order System**: Complete with customer details and audio recording

## 🚀 Ready to Use!

Your application will be accessible at:
- **Main Site**: http://localhost:3000
- **Frames**: http://localhost:3000/frames.html
- **Order Flow**: Complete working system

