#!/usr/bin/env python3
"""
Test Supabase connection and verify setup.
"""
import os
import sys
from decouple import config

# Add the backend directory to Python path
sys.path.append('backend')

def test_supabase_connection():
    """Test Supabase connection."""
    try:
        from supabase import create_client
        
        # Get Supabase credentials
        supabase_url = config('SUPABASE_URL')
        supabase_key = config('SUPABASE_ANON_KEY')
        
        print("🔗 Testing Supabase connection...")
        print(f"URL: {supabase_url}")
        print(f"Key: {supabase_key[:20]}...")
        
        # Create client
        supabase = create_client(supabase_url, supabase_key)
        
        # Test connection by trying to read from a table
        print("📊 Testing database connection...")
        
        # This will work once the schema is created
        try:
            result = supabase.table('api_frame').select('*').limit(1).execute()
            print(f"✅ Connection successful! Found {len(result.data)} frames.")
        except Exception as e:
            print(f"⚠️  Database not ready yet: {e}")
            print("💡 Make sure to run the SQL schema in Supabase first!")
        
        return True
        
    except ImportError:
        print("❌ Supabase client not installed. Run: pip install supabase")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_environment_variables():
    """Test environment variables."""
    print("🔧 Testing environment variables...")
    
    required_vars = [
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY',
        'DB_HOST',
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD'
    ]
    
    missing_vars = []
    for var in required_vars:
        try:
            value = config(var)
            if not value or value == f'your-{var.lower()}-here':
                missing_vars.append(var)
            else:
                print(f"✅ {var}: {value[:20] if len(value) > 20 else value}...")
        except:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing or invalid variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ All environment variables are set!")
    return True

if __name__ == "__main__":
    print("🚀 Supabase Connection Test")
    print("=" * 40)
    
    # Test environment variables
    env_ok = test_environment_variables()
    print()
    
    # Test Supabase connection
    if env_ok:
        connection_ok = test_supabase_connection()
    else:
        print("❌ Skipping connection test due to missing environment variables")
        connection_ok = False
    
    print()
    print("=" * 40)
    if env_ok and connection_ok:
        print("🎉 Supabase setup is ready!")
        print("📋 Next steps:")
        print("1. Run the SQL schema in Supabase SQL Editor")
        print("2. Start the application with: docker-compose -f docker-compose.supabase.yml up")
    else:
        print("⚠️  Setup needs attention:")
        if not env_ok:
            print("- Update your .env file with correct values")
        if not connection_ok:
            print("- Install Supabase client: pip install supabase")
            print("- Run the SQL schema in Supabase")
