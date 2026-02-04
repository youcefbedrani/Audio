#!/bin/bash

# Deploy Script for Audio Frame Art on VPS

echo "Starting deployment..."

# 1. Install Docker & Docker Compose if not present
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    
    # Add current user to docker group
    sudo usermod -aG docker $USER
    echo "Docker installed. You might need to log out and back in for group changes to take effect."
fi

# 2. Check for .env file
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "Please edit .env with your actual secrets!"
    else
        echo "WARNING: No .env.example found. Please create .env manually."
    fi
fi

# 3. Pull latest changes (if this is a git repo)
if [ -d .git ]; then
    echo "Pulling latest changes from git..."
    git pull origin main
else
    echo "Not a git repository or just a file copy. Skipping git pull."
fi

# 4. Build and Run
echo "Building and starting containers in detached mode..."
docker compose -f production.yml up --build -d

echo "Deployment complete!"
echo "Check status with: docker compose -f production.yml ps"
echo "View logs with: docker compose -f production.yml logs -f"
