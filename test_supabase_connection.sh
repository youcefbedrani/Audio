#!/bin/bash

echo "🔍 Testing Supabase Connection..."

# Test Supabase API directly
echo "📡 Testing Supabase API..."
curl -s "https://qksmfogjdurxgzmlcujb.supabase.co/rest/v1/api_frame" \
  -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrc21mb2dqZHVyeGd6bWxjdWpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA0NTg3OTEsImV4cCI6MjA3NjAzNDc5MX0.E1VDpkzcq3AzyPiNZOHU2_5IPyx2k76UdZZiaXg3CVk" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrc21mb2dqZHVyeGd6bWxjdWpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA0NTg3OTEsImV4cCI6MjA3NjAzNDc5MX0.E1VDpkzcq3AzyPiNZOHU2_5IPyx2k76UdZZiaXg3CVk" \
  | head -3

echo ""
echo "🔍 Testing Database Connection..."
echo "Host: db.qksmfogjdurxgzmlcujb.supabase.co"
echo "Port: 5432"
echo "Database: postgres"
echo "User: postgres"
echo "Password: pfg5jIjAYKpwYlwG"

echo ""
echo "📋 To fix the connection:"
echo "1. Check if Supabase project is active"
echo "2. Verify database password in Supabase dashboard"
echo "3. Check if database is accessible from external connections"
echo "4. Update .env file with correct credentials"

