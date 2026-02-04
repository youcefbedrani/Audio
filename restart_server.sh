#!/bin/bash
# Script to stop all API servers and start the updated supabase_docker_api.py

echo "🛑 Stopping all API servers on port 8001..."

# Kill any process using port 8001
fuser -k 8001/tcp 2>/dev/null || true
pkill -f "python.*supabase_docker_api" || true
pkill -f "python.*api.*8001" || true

sleep 2

# Verify port is free
if lsof -ti:8001 > /dev/null 2>&1; then
    echo "❌ Port 8001 still in use. Trying sudo..."
    sudo fuser -k 8001/tcp 2>/dev/null || true
    sleep 2
fi

# Check if port is now free
if ! lsof -ti:8001 > /dev/null 2>&1; then
    echo "✅ Port 8001 is free"
else
    echo "⚠️  Port 8001 may still be in use"
fi

echo ""
echo "🚀 Starting updated Supabase Docker API..."
echo "📝 Logs will be saved to api_server.log"
echo ""

# Start the server
cd "$(dirname "$0")"
nohup python3 supabase_docker_api.py > api_server.log 2>&1 &

sleep 3

# Test if server started
if curl -s http://localhost:8001/health/ > /dev/null 2>&1; then
    echo "✅ Server is running!"
    echo ""
    echo "🧪 Testing storage endpoint..."
    curl -s http://localhost:8001/api/test-storage/ | python3 -m json.tool 2>/dev/null || curl -s http://localhost:8001/api/test-storage/
    echo ""
    echo ""
    echo "📋 Available endpoints:"
    echo "  - Health: http://localhost:8001/health/"
    echo "  - Test Storage: http://localhost:8001/api/test-storage/"
    echo "  - View logs: tail -f api_server.log"
else
    echo "❌ Server failed to start. Check api_server.log for errors:"
    tail -20 api_server.log
fi

