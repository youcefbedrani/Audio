#!/bin/bash
# Quick script to build and start Docker with waveform code generation

echo "🐳 Building Docker image with waveform code generation..."
docker-compose build api

echo ""
echo "🚀 Starting Docker container..."
docker-compose up -d api

echo ""
echo "📋 Container status:"
docker-compose ps api

echo ""
echo "📝 View logs with: docker-compose logs -f api"
echo "🛑 Stop with: docker-compose down"
echo ""
echo "🧪 Test endpoints:"
echo "  Health: curl http://localhost:8001/health/"
echo "  Storage: curl http://localhost:8001/api/test-storage/"
