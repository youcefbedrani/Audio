#!/usr/bin/env python3
"""
Setup Cloudinary for Audio Frame Art
"""

import os
import sys

def setup_cloudinary():
    """Setup Cloudinary credentials"""
    print("☁️  CLOUDINARY SETUP FOR AUDIO FRAME ART")
    print("=" * 50)
    
    print("\n📋 To get your Cloudinary credentials:")
    print("1. Go to: https://cloudinary.com/console")
    print("2. Sign up or log in to your account")
    print("3. Go to Dashboard > Settings > API Keys")
    print("4. Copy your Cloud Name, API Key, and API Secret")
    
    print("\n🔧 Enter your Cloudinary credentials:")
    
    cloud_name = input("Cloud Name: ").strip()
    api_key = input("API Key: ").strip()
    api_secret = input("API Secret: ").strip()
    
    if not cloud_name or not api_key or not api_secret:
        print("❌ All credentials are required!")
        return False
    
    # Update the working_audio_api.py file
    try:
        with open("working_audio_api.py", "r") as f:
            content = f.read()
        
        # Replace placeholder values
        content = content.replace('CLOUDINARY_CLOUD_NAME = "your_cloud_name"', f'CLOUDINARY_CLOUD_NAME = "{cloud_name}"')
        content = content.replace('CLOUDINARY_API_KEY = "your_api_key"', f'CLOUDINARY_API_KEY = "{api_key}"')
        content = content.replace('CLOUDINARY_API_SECRET = "your_api_secret"', f'CLOUDINARY_API_SECRET = "{api_secret}"')
        
        with open("working_audio_api.py", "w") as f:
            f.write(content)
        
        print("✅ Cloudinary credentials updated in working_audio_api.py")
        
        # Test the connection
        print("\n🧪 Testing Cloudinary connection...")
        try:
            import cloudinary
            import cloudinary.uploader
            from cloudinary import api as cloudinary_api
            
            cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret
            )
            
            # Test connection
            result = cloudinary_api.ping()
            print("✅ Cloudinary connection successful!")
            print(f"   Status: {result.get('status', 'unknown')}")
            
            return True
            
        except ImportError:
            print("❌ Cloudinary library not installed!")
            print("   Install with: pip install cloudinary")
            return False
        except Exception as e:
            print(f"❌ Cloudinary connection failed: {e}")
            print("   Please check your credentials and try again")
            return False
            
    except Exception as e:
        print(f"❌ Error updating file: {e}")
        return False

def test_upload():
    """Test file upload to Cloudinary"""
    print("\n🧪 Testing file upload to Cloudinary...")
    
    try:
        import cloudinary
        import cloudinary.uploader
        
        # Create a test file
        test_content = "This is a test audio file for Audio Frame Art"
        with open("test_cloudinary.txt", "w") as f:
            f.write(test_content)
        
        # Upload test file
        result = cloudinary.uploader.upload(
            "test_cloudinary.txt",
            folder="audio_frame_art/test",
            resource_type="raw"
        )
        
        print(f"✅ Test upload successful!")
        print(f"   URL: {result['secure_url']}")
        print(f"   Public ID: {result['public_id']}")
        
        # Clean up
        os.remove("test_cloudinary.txt")
        
        return True
        
    except Exception as e:
        print(f"❌ Test upload failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Cloudinary setup...")
    
    if setup_cloudinary():
        print("\n🎉 Cloudinary setup completed successfully!")
        
        # Ask if user wants to test upload
        test = input("\n🧪 Test file upload? (y/n): ").strip().lower()
        if test == 'y':
            test_upload()
        
        print("\n📋 Next steps:")
        print("1. Restart your API: docker-compose up -d --build")
        print("2. Test audio upload with a real order")
        print("3. Check that files appear in your Cloudinary dashboard")
        
    else:
        print("\n❌ Cloudinary setup failed!")
        print("Please check your credentials and try again.")
