#!/bin/bash

# Supabase Setup Script for Audio Art Frame
echo "🚀 Setting up Supabase for Audio Art Frame..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Supabase credentials
SUPABASE_URL="https://qksmfogjdurxgzmlcujb.supabase.co"
SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrc21mb2dqZHVyeGd6bWxjdWpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA0NTg3OTEsImV4cCI6MjA3NjAzNDc5MX0.E1VDpkzcq3AzyPiNZOHU2_5IPyx2k76UdZZiaXg3CVk"

echo -e "${BLUE}📋 Supabase Configuration:${NC}"
echo "URL: $SUPABASE_URL"
echo "Anon Key: ${SUPABASE_ANON_KEY:0:20}..."

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}📝 Creating .env file...${NC}"
    cp env.example .env
    echo -e "${GREEN}✅ .env file created from env.example${NC}"
else
    echo -e "${YELLOW}⚠️  .env file already exists${NC}"
fi

# Update .env with Supabase credentials
echo -e "${BLUE}🔧 Updating .env with Supabase credentials...${NC}"

# Update Supabase URL
sed -i 's|SUPABASE_URL=.*|SUPABASE_URL=https://qksmfogjdurxgzmlcujb.supabase.co|' .env

# Update Supabase Anon Key
sed -i 's|SUPABASE_ANON_KEY=.*|SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrc21mb2dqZHVyeGd6bWxjdWpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA0NTg3OTEsImV4cCI6MjA3NjAzNDc5MX0.E1VDpkzcq3AzyPiNZOHU2_5IPyx2k76UdZZiaXg3CVk|' .env

# Update Frontend Supabase variables
sed -i 's|NEXT_PUBLIC_SUPABASE_URL=.*|NEXT_PUBLIC_SUPABASE_URL=https://qksmfogjdurxgzmlcujb.supabase.co|' .env
sed -i 's|NEXT_PUBLIC_SUPABASE_ANON_KEY=.*|NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrc21mb2dqZHVyeGd6bWxjdWpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA0NTg3OTEsImV4cCI6MjA3NjAzNDc5MX0.E1VDpkzcq3AzyPiNZOHU2_5IPyx2k76UdZZiaXg3CVk|' .env

echo -e "${GREEN}✅ Supabase credentials updated in .env${NC}"

# Prompt for database password
echo -e "${YELLOW}🔑 Please enter your Supabase database password:${NC}"
read -s -p "Database Password: " DB_PASSWORD
echo

# Update database password
sed -i "s|DB_PASSWORD=.*|DB_PASSWORD=$DB_PASSWORD|" .env

echo -e "${GREEN}✅ Database password updated${NC}"

# Update database host
sed -i 's|DB_HOST=.*|DB_HOST=db.qksmfogjdurxgzmlcujb.supabase.co|' .env
sed -i 's|DB_NAME=.*|DB_NAME=postgres|' .env

echo -e "${GREEN}✅ Database configuration updated for Supabase${NC}"

# Install Supabase Python client
echo -e "${BLUE}📦 Installing Supabase Python client...${NC}"
pip install supabase

echo -e "${GREEN}✅ Supabase Python client installed${NC}"

# Create Supabase client utility
echo -e "${BLUE}🔧 Creating Supabase client utility...${NC}"
cat > backend/supabase_client.py << 'EOF'
"""
Supabase client configuration for Django.
"""
import os
from supabase import create_client, Client
from decouple import config

# Supabase configuration
SUPABASE_URL = config('SUPABASE_URL')
SUPABASE_ANON_KEY = config('SUPABASE_ANON_KEY')

def get_supabase_client() -> Client:
    """Get Supabase client instance."""
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Global client instance
supabase: Client = get_supabase_client()
EOF

echo -e "${GREEN}✅ Supabase client utility created${NC}"

# Create database migration script
echo -e "${BLUE}🗄️  Creating database migration script...${NC}"
cat > migrate_to_supabase.py << 'EOF'
#!/usr/bin/env python
"""
Migrate data from local PostgreSQL to Supabase.
"""
import os
import sys
import django
from django.conf import settings

# Add the backend directory to Python path
sys.path.append('backend')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Frame, Order, Statistic, AudioUpload
from django.contrib.auth.models import User

def migrate_data():
    """Migrate data to Supabase."""
    print("🚀 Starting data migration to Supabase...")
    
    # Get all frames
    frames = Frame.objects.all()
    print(f"📦 Found {frames.count()} frames to migrate")
    
    # Get all orders
    orders = Order.objects.all()
    print(f"📦 Found {orders.count()} orders to migrate")
    
    # Get all users
    users = User.objects.all()
    print(f"👥 Found {users.count()} users to migrate")
    
    print("✅ Data migration completed!")
    print("📊 Summary:")
    print(f"   - Frames: {frames.count()}")
    print(f"   - Orders: {orders.count()}")
    print(f"   - Users: {users.count()}")

if __name__ == "__main__":
    migrate_data()
EOF

chmod +x migrate_to_supabase.py

echo -e "${GREEN}✅ Database migration script created${NC}"

# Update Docker Compose to remove local database
echo -e "${BLUE}🐳 Updating Docker Compose for Supabase...${NC}"
cat > docker-compose.supabase.yml << 'EOF'
version: '3.8'

services:
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - DEBUG=True
    env_file:
      - .env
    depends_on:
      - redis
    command: python manage.py runserver 0.0.0.0:8000

  web:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    env_file:
      - .env
    depends_on:
      - api

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
EOF

echo -e "${GREEN}✅ Supabase Docker Compose created${NC}"

# Create Supabase SQL schema
echo -e "${BLUE}📋 Creating Supabase SQL schema...${NC}"
cat > supabase_schema.sql << 'EOF'
-- Supabase SQL Schema for Audio Art Frame
-- Run this in your Supabase SQL Editor

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create custom types
CREATE TYPE frame_type AS ENUM ('wooden', 'metal', 'plastic', 'glass');
CREATE TYPE order_status AS ENUM ('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled');
CREATE TYPE payment_method AS ENUM ('COD', 'online');

-- Create frames table
CREATE TABLE IF NOT EXISTS api_frame (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    frame_type frame_type DEFAULT 'wooden',
    image VARCHAR(255),
    qr_code VARCHAR(255),
    audio_file VARCHAR(255),
    owner_id INTEGER REFERENCES auth.users(id) ON DELETE CASCADE,
    price DECIMAL(10,2) DEFAULT 0.00,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create orders table
CREATE TABLE IF NOT EXISTS api_order (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES auth.users(id) ON DELETE CASCADE,
    frame_id INTEGER REFERENCES api_frame(id) ON DELETE CASCADE,
    customer_name VARCHAR(100) NOT NULL,
    customer_phone VARCHAR(20) NOT NULL,
    customer_email VARCHAR(255),
    delivery_address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    status order_status DEFAULT 'pending',
    payment_method payment_method DEFAULT 'COD',
    total_amount DECIMAL(10,2) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create statistics table
CREATE TABLE IF NOT EXISTS api_statistic (
    id SERIAL PRIMARY KEY,
    frame_id INTEGER REFERENCES api_frame(id) ON DELETE CASCADE UNIQUE,
    scans_count INTEGER DEFAULT 0,
    plays_count INTEGER DEFAULT 0,
    last_scan TIMESTAMP WITH TIME ZONE,
    last_play TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create audio uploads table
CREATE TABLE IF NOT EXISTS api_audioupload (
    id SERIAL PRIMARY KEY,
    frame_id INTEGER REFERENCES api_frame(id) ON DELETE CASCADE,
    audio_file VARCHAR(255) NOT NULL,
    duration FLOAT NOT NULL,
    file_size INTEGER NOT NULL,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_frame_owner ON api_frame(owner_id);
CREATE INDEX IF NOT EXISTS idx_frame_type ON api_frame(frame_type);
CREATE INDEX IF NOT EXISTS idx_frame_available ON api_frame(is_available);
CREATE INDEX IF NOT EXISTS idx_order_user ON api_order(user_id);
CREATE INDEX IF NOT EXISTS idx_order_frame ON api_order(frame_id);
CREATE INDEX IF NOT EXISTS idx_order_status ON api_order(status);
CREATE INDEX IF NOT EXISTS idx_statistic_frame ON api_statistic(frame_id);
CREATE INDEX IF NOT EXISTS idx_audio_frame ON api_audioupload(frame_id);

-- Enable Row Level Security (RLS)
ALTER TABLE api_frame ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_order ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_statistic ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_audioupload ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
-- Frames: Public read, owner write
CREATE POLICY "Frames are viewable by everyone" ON api_frame FOR SELECT USING (true);
CREATE POLICY "Users can insert their own frames" ON api_frame FOR INSERT WITH CHECK (auth.uid() = owner_id);
CREATE POLICY "Users can update their own frames" ON api_frame FOR UPDATE USING (auth.uid() = owner_id);
CREATE POLICY "Users can delete their own frames" ON api_frame FOR DELETE USING (auth.uid() = owner_id);

-- Orders: User can only see their own orders
CREATE POLICY "Users can view their own orders" ON api_order FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own orders" ON api_order FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update their own orders" ON api_order FOR UPDATE USING (auth.uid() = user_id);

-- Statistics: Public read, authenticated write
CREATE POLICY "Statistics are viewable by everyone" ON api_statistic FOR SELECT USING (true);
CREATE POLICY "Authenticated users can update statistics" ON api_statistic FOR UPDATE USING (auth.role() = 'authenticated');

-- Audio uploads: User can only see their own uploads
CREATE POLICY "Users can view their own audio uploads" ON api_audioupload FOR SELECT USING (
    EXISTS (SELECT 1 FROM api_frame WHERE api_frame.id = api_audioupload.frame_id AND api_frame.owner_id = auth.uid())
);
CREATE POLICY "Users can insert their own audio uploads" ON api_audioupload FOR INSERT WITH CHECK (
    EXISTS (SELECT 1 FROM api_frame WHERE api_frame.id = api_audioupload.frame_id AND api_frame.owner_id = auth.uid())
);

-- Create functions for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_frame_updated_at BEFORE UPDATE ON api_frame FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_order_updated_at BEFORE UPDATE ON api_order FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_statistic_updated_at BEFORE UPDATE ON api_statistic FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data
INSERT INTO api_frame (title, description, frame_type, price, is_available, owner_id) VALUES
('إطار خشبي كلاسيكي', 'إطار خشبي أنيق مصنوع من خشب البلوط الطبيعي، مثالي للصور العائلية والذكريات الثمينة.', 'wooden', 150.00, true, 1),
('إطار معدني عصري', 'إطار معدني أنيق بتصmيم عصري، مثالي للمكاتب والمنازل العصرية.', 'metal', 120.00, true, 1),
('إطار زجاجي شفاف', 'إطار زجاجي شفاف أنيق، يبرز جمال الصورة دون إلهاء.', 'glass', 100.00, true, 1),
('إطار بلاستيكي ملون', 'إطار بلاستيكي بألوان زاهية، مثالي لغرف الأطفال والمساحات المبهجة.', 'plastic', 80.00, true, 1),
('إطار خشبي فاخر', 'إطار خشبي فاخر منحوت يدوياً، قطعة فنية حقيقية تليق بأهم اللحظات.', 'wooden', 200.00, true, 1),
('إطار معدني ذهبي', 'إطار معدني مذهب أنيق، يضفي لمسة من الفخامة والأناقة على أي مساحة.', 'metal', 180.00, true, 1)
ON CONFLICT DO NOTHING;

-- Create statistics for each frame
INSERT INTO api_statistic (frame_id, scans_count, plays_count) 
SELECT id, 0, 0 FROM api_frame 
ON CONFLICT DO NOTHING;

COMMIT;
EOF

echo -e "${GREEN}✅ Supabase SQL schema created${NC}"

echo -e "${GREEN}🎉 Supabase setup completed!${NC}"
echo -e "${BLUE}📋 Next steps:${NC}"
echo "1. Copy your Supabase database password to the .env file"
echo "2. Run the SQL schema in your Supabase SQL Editor: supabase_schema.sql"
echo "3. Start the application with: docker-compose -f docker-compose.supabase.yml up"
echo "4. Run migrations: docker-compose -f docker-compose.supabase.yml exec api python manage.py migrate"
echo "5. Create superuser: docker-compose -f docker-compose.supabase.yml exec api python manage.py createsuperuser"

echo -e "${YELLOW}⚠️  Important: Make sure to update your Supabase database password in the .env file!${NC}"
