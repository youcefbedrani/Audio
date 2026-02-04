#!/usr/bin/env python3
"""
Setup Cloudinary credentials for the Audio Frame Art API
"""

import os

def setup_cloudinary():
    print("🔧 Setting up Cloudinary credentials...")
    print("\nTo get your Cloudinary credentials:")
    print("1. Go to: https://cloudinary.com/console")
    print("2. Sign up or log in")
    print("3. Go to Dashboard")
    print("4. Copy your Cloud Name, API Key, and API Secret")
    
    print("\n" + "="*50)
    print("CURRENT CLOUDINARY CONFIGURATION:")
    print("="*50)
    
    # Read current config
    with open('complete_audio_api.py', 'r') as f:
        content = f.read()
    
    # Extract current values
    cloud_name_line = [line for line in content.split('\n') if 'CLOUDINARY_CLOUD_NAME' in line][0]
    api_key_line = [line for line in content.split('\n') if 'CLOUDINARY_API_KEY' in line][0]
    api_secret_line = [line for line in content.split('\n') if 'CLOUDINARY_API_SECRET' in line][0]
    
    print(f"Cloud Name: {cloud_name_line.split('=')[1].strip()}")
    print(f"API Key: {api_key_line.split('=')[1].strip()}")
    print(f"API Secret: {api_secret_line.split('=')[1].strip()}")
    
    print("\n" + "="*50)
    print("TO UPDATE CREDENTIALS:")
    print("="*50)
    print("Edit the file 'complete_audio_api.py' and update these lines:")
    print("CLOUDINARY_CLOUD_NAME = 'your-actual-cloud-name'")
    print("CLOUDINARY_API_KEY = 'your-actual-api-key'")
    print("CLOUDINARY_API_SECRET = 'your-actual-api-secret'")
    
    print("\n" + "="*50)
    print("TESTING CLOUDINARY CONNECTION:")
    print("="*50)
    
    try:
        import cloudinary
        import cloudinary.uploader
        
        # Test with current credentials
        cloudinary.config(
            cloud_name="dulct8pma",
            api_key="your-api-key",
            api_secret="your-api-secret"
        )
        
        # Try to get account info
        from cloudinary import api as cloudinary_api
        result = cloudinary_api.ping()
        print("✅ Cloudinary connection successful!")
        print(f"Response: {result}")
        
    except Exception as e:
        print("❌ Cloudinary connection failed!")
        print(f"Error: {e}")
        print("\nThis is expected if you haven't updated the credentials yet.")
    
    print("\n" + "="*50)
    print("NEXT STEPS:")
    print("="*50)
    print("1. Update Cloudinary credentials in complete_audio_api.py")
    print("2. Rebuild Docker container: docker-compose up -d --build")
    print("3. Test audio upload: curl -X POST http://localhost:8001/api/orders/ -F 'audio_file=@test.mp3' ...")

if __name__ == "__main__":
    setup_cloudinary()
