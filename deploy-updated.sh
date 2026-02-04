#!/bin/bash

echo "🚀 Audio Frame Art - Updated Docker Deployment"
echo "=============================================="

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.prod.yml down

# Remove old images
echo "🧹 Cleaning up old images..."
docker system prune -f

# Build and start services
echo "🔨 Building and starting services..."

# Check if development mode is requested
if [ "$1" = "dev" ]; then
    echo "📱 Starting in DEVELOPMENT mode..."
    docker-compose -f docker-compose.dev.yml up --build -d
    echo ""
    echo "✅ Development environment ready!"
    echo "🌐 Frontend: http://localhost:3000"
    echo "🔌 API: http://localhost:8001"
    echo "📊 API Health: http://localhost:8001/health/"
    
elif [ "$1" = "prod" ]; then
    echo "🏭 Starting in PRODUCTION mode..."
    docker-compose -f docker-compose.prod.yml up --build -d
    echo ""
    echo "✅ Production environment ready!"
    echo "🌐 Website: http://localhost:3000"
    echo "🔌 API: http://localhost:8001"
    
else
    echo "🚀 Starting in STANDARD mode..."
    docker-compose up --build -d
    echo ""
    echo "✅ Standard environment ready!"
    echo "🌐 Frontend: http://localhost:3000"
    echo "🔌 API: http://localhost:8001"
    echo "📊 API Health: http://localhost:8001/health/"
fi

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Test API health
echo "🔍 Testing API health..."
if curl -s http://localhost:8001/health/ > /dev/null; then
    echo "✅ API is healthy!"
else
    echo "❌ API health check failed"
fi

# Test frontend
echo "🔍 Testing frontend..."
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is accessible!"
else
    echo "❌ Frontend check failed"
fi

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "📋 Available endpoints:"
echo "  🌐 Frontend: http://localhost:3000"
echo "  🔌 API: http://localhost:8001"
echo "  📊 Health: http://localhost:8001/health/"
echo "  📡 Frames: http://localhost:8001/api/frames/"
echo "  📦 Orders: http://localhost:8001/api/orders/"
echo ""
echo "🛠️ Management commands:"
echo "  📊 View logs: docker-compose logs -f"
echo "  🛑 Stop: docker-compose down"
echo "  🔄 Restart: docker-compose restart"
echo ""
echo "🎨 Your Audio Frame Art system is ready!"
