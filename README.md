# Audio Art Frame

A complete production-ready system for physical art frames with QR code-linked audio messages.

## Architecture

- **Frontend**: Next.js + Tailwind CSS + TypeScript
- **Backend**: Django REST Framework + PostgreSQL
- **Mobile**: Flutter
- **Storage**: Cloudinary
- **Deployment**: Docker + Nginx

## Quick Start

1. **Setup Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Cloudinary credentials and other settings
   ```

2. **Run with Docker**
   ```bash
   docker-compose up --build
   ```

3. **Access Applications**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Admin: http://localhost:8000/admin

## Project Structure

```
├── backend/          # Django REST API
├── frontend/         # Next.js web app
├── mobile/           # Flutter mobile app
├── docker/           # Docker configuration
├── docker-compose.yml
└── nginx.conf
```

## Features

- 🖼️ Browse and select art frames
- 🎵 Upload or record audio messages
- 📱 QR code scanning with mobile app
- 📊 Admin dashboard with analytics
- 🚚 Cash on delivery orders
- 🔒 JWT authentication
- ☁️ Cloudinary file storage

## Development

See individual README files in each directory for specific setup instructions.
