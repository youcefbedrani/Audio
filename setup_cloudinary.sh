#!/bin/bash

# Audio Art Frame - Cloudinary Setup Script
echo "🌩️  Audio Art Frame - Cloudinary Setup"
echo "======================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo "You have Cloudinary cloud name: ${GREEN}dulct8pma${NC}"
echo ""
echo "To complete the setup, you need to:"
echo "1. Go to https://cloudinary.com/console"
echo "2. Login to your account"
echo "3. Copy your API Key and API Secret"
echo "4. Run this script with your credentials"
echo ""

# Get API Key
echo -n "Enter your Cloudinary API Key: "
read API_KEY

# Get API Secret
echo -n "Enter your Cloudinary API Secret: "
read API_SECRET

# Validate inputs
if [ -z "$API_KEY" ] || [ -z "$API_SECRET" ]; then
    echo -e "${RED}❌ API Key and API Secret are required${NC}"
    exit 1
fi

# Update .env file
echo ""
echo "Updating .env file..."

# Create backup
cp .env .env.backup

# Update Cloudinary settings
sed -i "s/CLOUDINARY_URL=.*/CLOUDINARY_URL=cloudinary:\/\/${API_KEY}:${API_SECRET}@dulct8pma/" .env
sed -i "s/CLOUDINARY_CLOUD_NAME=.*/CLOUDINARY_CLOUD_NAME=dulct8pma/" .env
sed -i "s/CLOUDINARY_API_KEY=.*/CLOUDINARY_API_KEY=${API_KEY}/" .env
sed -i "s/CLOUDINARY_API_SECRET=.*/CLOUDINARY_API_SECRET=${API_SECRET}/" .env
sed -i "s/NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME=.*/NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME=dulct8pma/" .env

echo -e "${GREEN}✅ .env file updated successfully!${NC}"
echo ""
echo "Your Cloudinary configuration:"
echo "  Cloud Name: dulct8pma"
echo "  API Key: ${API_KEY}"
echo "  API Secret: ${API_SECRET:0:8}..."
echo ""
echo "Next steps:"
echo "1. Run: docker-compose -f docker-compose.dev.yml up --build"
echo "2. Access: http://localhost:3000 (frontend)"
echo "3. Access: http://localhost:8000/admin (admin)"
echo ""
echo "Backup of original .env saved as .env.backup"
