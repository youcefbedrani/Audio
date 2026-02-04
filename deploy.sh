#!/bin/bash

# Audio Art Frame Deployment Script
# This script helps deploy the application to a VPS

set -e

echo "🚀 Audio Art Frame Deployment Script"
echo "====================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please create a .env file with your configuration."
    echo "You can copy env.example to .env and update the values."
    exit 1
fi

# Load environment variables
source .env

echo "📋 Configuration:"
echo "  - Database: $DB_NAME"
echo "  - Cloudinary: $CLOUDINARY_CLOUD_NAME"
echo "  - Debug: $DEBUG"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo "Please install Docker and Docker Compose first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed!"
    echo "Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create SSL directory if it doesn't exist
mkdir -p ssl

# Check if SSL certificates exist
if [ ! -f ssl/cert.pem ] || [ ! -f ssl/key.pem ]; then
    echo "⚠️  SSL certificates not found!"
    echo "Creating self-signed certificates for development..."
    echo "For production, replace these with real certificates."
    
    openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    
    echo "✅ Self-signed certificates created"
else
    echo "✅ SSL certificates found"
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

# Run database migrations
echo "🗄️  Running database migrations..."
docker-compose exec api python manage.py migrate

# Create superuser (optional)
echo "👤 Do you want to create a superuser? (y/n)"
read -r create_superuser
if [ "$create_superuser" = "y" ] || [ "$create_superuser" = "Y" ]; then
    docker-compose exec api python manage.py createsuperuser
fi

# Collect static files
echo "📁 Collecting static files..."
docker-compose exec api python manage.py collectstatic --noinput

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📱 Your Audio Art Frame application is now running:"
echo "  - Frontend: https://localhost (or your domain)"
echo "  - Backend API: https://localhost/api/"
echo "  - Admin: https://localhost/admin/"
echo ""
echo "📋 Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop services: docker-compose down"
echo "  - Restart services: docker-compose restart"
echo "  - Update application: ./deploy.sh"
echo ""
echo "🔧 For production deployment:"
echo "  1. Update .env with production values"
echo "  2. Replace SSL certificates in ssl/ directory"
echo "  3. Configure your domain in nginx.conf"
echo "  4. Set up proper backup for PostgreSQL data"
echo ""
