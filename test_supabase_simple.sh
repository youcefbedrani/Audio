#!/bin/bash

# Simple Supabase Test Script
# Run this after creating the database schema

echo "🚀 Testing Supabase Database..."

# Supabase credentials
SUPABASE_URL="https://qksmfogjdurxgzmlcujb.supabase.co"
API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrc21mb2dqZHVyeGd6bWxjdWpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA0NTg3OTEsImV4cCI6MjA3NjAzNDc5MX0.E1VDpkzcq3AzyPiNZOHU2_5IPyx2k76UdZZiaXg3CVk"

echo "🔗 Testing connection..."
response=$(curl -s -w "%{http_code}" -o /tmp/supabase_test.json \
  -H "apikey: $API_KEY" \
  -H "Authorization: Bearer $API_KEY" \
  "$SUPABASE_URL/rest/v1/api_frame?select=*&limit=1")

if [ "$response" = "200" ]; then
    echo "✅ Connection successful!"
    
    # Check if we have data
    frames_count=$(cat /tmp/supabase_test.json | jq '. | length' 2>/dev/null || echo "0")
    
    if [ "$frames_count" -gt 0 ]; then
        echo "✅ Database schema created successfully!"
        echo "📊 Found $frames_count frames"
        
        # Show first frame
        echo "🖼️  Sample frame:"
        cat /tmp/supabase_test.json | jq '.[0] | {title, frame_type, price}' 2>/dev/null || echo "Could not parse frame data"
        
        echo ""
        echo "🎉 SUPABASE IS READY!"
        echo "📋 Next steps:"
        echo "1. Start your application: docker-compose -f docker-compose.supabase.yml up"
        echo "2. Run migrations: docker-compose -f docker-compose.supabase.yml exec api python manage.py migrate"
        echo "3. Create admin user: docker-compose -f docker-compose.supabase.yml exec api python manage.py createsuperuser"
        
    else
        echo "⚠️  Database connected but no frames found"
        echo "💡 Make sure you ran the SQL schema in Supabase SQL Editor"
    fi
    
else
    echo "❌ Connection failed (HTTP $response)"
    echo "💡 Check your Supabase credentials and make sure the schema is created"
fi

# Clean up
rm -f /tmp/supabase_test.json

echo ""
echo "🔧 To create the schema:"
echo "1. Go to: https://supabase.com/dashboard/project/qksmfogjdurxgzmlcujb"
echo "2. Click 'SQL Editor'"
echo "3. Copy and paste the contents of 'supabase_schema.sql'"
echo "4. Click 'Run'"
