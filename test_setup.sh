#!/bin/bash

# Audio Art Frame - Setup Test Script
echo "🧪 Audio Art Frame - Setup Test Script"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ $2 -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
    else
        echo -e "${RED}❌ $1${NC}"
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Test 1: Check if .env file exists
echo ""
echo "📋 Testing Environment Configuration..."
if [ -f .env ]; then
    print_status ".env file exists" 0
else
    print_status ".env file exists" 1
    echo "   Please create .env file from env.example"
    exit 1
fi

# Test 2: Check if Cloudinary is configured
echo ""
echo "🌩️  Testing Cloudinary Configuration..."
if grep -q "CLOUDINARY_CLOUD_NAME=your-cloud-name" .env; then
    print_warning "Cloudinary not configured - this is REQUIRED"
    echo "   Please update .env with your Cloudinary credentials"
    echo "   Get them from: https://cloudinary.com/console"
else
    print_status "Cloudinary appears to be configured" 0
fi

# Test 3: Check Docker installation
echo ""
echo "🐳 Testing Docker Installation..."
if command -v docker &> /dev/null; then
    print_status "Docker is installed" 0
    docker --version
else
    print_status "Docker is installed" 1
    echo "   Please install Docker first"
fi

if command -v docker-compose &> /dev/null; then
    print_status "Docker Compose is installed" 0
    docker-compose --version
else
    print_status "Docker Compose is installed" 1
    echo "   Please install Docker Compose first"
fi

# Test 4: Check Python installation
echo ""
echo "🐍 Testing Python Installation..."
if command -v python3 &> /dev/null; then
    print_status "Python 3 is installed" 0
    python3 --version
else
    print_status "Python 3 is installed" 1
    echo "   Please install Python 3 first"
fi

# Test 5: Check Node.js installation
echo ""
echo "📦 Testing Node.js Installation..."
if command -v node &> /dev/null; then
    print_status "Node.js is installed" 0
    node --version
else
    print_status "Node.js is installed" 1
    echo "   Please install Node.js first"
fi

if command -v npm &> /dev/null; then
    print_status "npm is installed" 0
    npm --version
else
    print_status "npm is installed" 1
    echo "   Please install npm first"
fi

# Test 6: Check Flutter installation
echo ""
echo "📱 Testing Flutter Installation..."
if command -v flutter &> /dev/null; then
    print_status "Flutter is installed" 0
    flutter --version | head -1
else
    print_status "Flutter is installed" 1
    echo "   Please install Flutter first"
fi

# Test 7: Test Backend Syntax
echo ""
echo "🔧 Testing Backend Code..."
cd backend
if python3 -m py_compile core/settings.py core/urls.py manage.py 2>/dev/null; then
    print_status "Backend Python syntax is valid" 0
else
    print_status "Backend Python syntax is valid" 1
fi
cd ..

# Test 8: Test Frontend Build
echo ""
echo "🌐 Testing Frontend Code..."
cd frontend
if npm run build >/dev/null 2>&1; then
    print_status "Frontend builds successfully" 0
else
    print_status "Frontend builds successfully" 1
    echo "   Run 'npm run build' to see detailed errors"
fi
cd ..

# Test 9: Test Flutter Analysis
echo ""
echo "📱 Testing Mobile Code..."
cd mobile
if flutter analyze >/dev/null 2>&1; then
    print_status "Flutter code analysis passes" 0
else
    print_warning "Flutter code has warnings (but should work)"
    echo "   Run 'flutter analyze' to see details"
fi
cd ..

# Test 10: Check if ports are free
echo ""
echo "🔌 Testing Port Availability..."
if lsof -i :3000 >/dev/null 2>&1; then
    print_warning "Port 3000 is in use"
else
    print_status "Port 3000 is available" 0
fi

if lsof -i :8000 >/dev/null 2>&1; then
    print_warning "Port 8000 is in use"
else
    print_status "Port 8000 is available" 0
fi

if lsof -i :5432 >/dev/null 2>&1; then
    print_warning "Port 5432 is in use"
else
    print_status "Port 5432 is available" 0
fi

# Summary
echo ""
echo "📊 Test Summary"
echo "==============="
echo ""
echo "🎯 Next Steps:"
echo "1. Configure Cloudinary credentials in .env file"
echo "2. Run: docker-compose -f docker-compose.dev.yml up --build"
echo "3. Access: http://localhost:3000 (frontend)"
echo "4. Access: http://localhost:8000/admin (admin)"
echo ""
echo "📚 For detailed setup instructions, see:"
echo "   - SETUP_GUIDE.md"
echo "   - TESTING_GUIDE.md"
echo "   - DEVELOPMENT.md"
echo ""
echo "🚀 Ready to deploy? Run: ./deploy.sh"
