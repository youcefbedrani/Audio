-- Supabase Database Schema for Audio Frame Art
-- Run this in your Supabase SQL Editor

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    id BIGSERIAL PRIMARY KEY,
    customer_name TEXT NOT NULL,
    customer_phone TEXT NOT NULL,
    customer_email TEXT DEFAULT '',
    delivery_address TEXT NOT NULL,
    city TEXT NOT NULL,
    postal_code TEXT DEFAULT '',
    wilaya TEXT DEFAULT '',
    baladya TEXT DEFAULT '',
    frame_id INTEGER NOT NULL,
    frame_title TEXT NOT NULL,
    frame_type TEXT NOT NULL,
    audio_file_url TEXT,
    status TEXT DEFAULT 'pending',
    payment_method TEXT DEFAULT 'COD',
    total_amount DECIMAL(10,2) NOT NULL,
    notes TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create frames table
CREATE TABLE IF NOT EXISTS frames (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    frame_type TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    image_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert sample frames
INSERT INTO frames (id, title, description, frame_type, price, is_available, image_url) VALUES
(1, 'إطار خشبي كلاسيكي', 'إطار خشبي أنيق مصنوع من خشب البلوط الطبيعي، مثالي للصور العائلية والذكريات الثمينة.', 'wooden', 150.00, TRUE, 'https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400'),
(2, 'إطار معدني عصري', 'إطار معدني أنيق بتصميم عصري، مثالي للمكاتب والمنازل العصرية.', 'metal', 120.00, TRUE, 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400'),
(3, 'إطار زجاجي شفاف', 'إطار زجاجي شفاف أنيق، يبرز جمال الصورة دون إلهاء.', 'glass', 100.00, TRUE, 'https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400'),
(4, 'إطار بلاستيكي ملون', 'إطار بلاستيكي بألوان زاهية، مثالي لغرف الأطفال والمساحات المبهجة.', 'plastic', 80.00, TRUE, 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400'),
(5, 'إطار خشبي فاخر', 'إطار خشبي فاخر منحوت يدوياً، قطعة فنية حقيقية تليق بأهم اللحظات.', 'wooden', 200.00, TRUE, 'https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400'),
(6, 'إطار معدني ذهبي', 'إطار معدني مذهب أنيق، يضفي لمسة من الفخامة والأناقة على أي مساحة.', 'metal', 180.00, TRUE, 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400')
ON CONFLICT (id) DO NOTHING;

-- Create statistics table
CREATE TABLE IF NOT EXISTS statistics (
    id BIGSERIAL PRIMARY KEY,
    frame_id INTEGER NOT NULL,
    scans_count INTEGER DEFAULT 0,
    plays_count INTEGER DEFAULT 0,
    last_scan TIMESTAMP WITH TIME ZONE,
    last_play TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security (RLS)
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE frames ENABLE ROW LEVEL SECURITY;
ALTER TABLE statistics ENABLE ROW LEVEL SECURITY;

-- Create policies for public access (for demo purposes)
-- In production, you should create proper user-based policies

-- Allow public read access to frames
CREATE POLICY "Allow public read access to frames" ON frames
    FOR SELECT USING (true);

-- Allow public insert access to orders
CREATE POLICY "Allow public insert access to orders" ON orders
    FOR INSERT WITH CHECK (true);

-- Allow public read access to orders (for admin purposes)
CREATE POLICY "Allow public read access to orders" ON orders
    FOR SELECT USING (true);

-- Allow public access to statistics
CREATE POLICY "Allow public access to statistics" ON statistics
    FOR ALL USING (true);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_orders_frame_id ON orders(frame_id);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_frames_frame_type ON frames(frame_type);
CREATE INDEX IF NOT EXISTS idx_frames_is_available ON frames(is_available);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers to automatically update updated_at
CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_frames_updated_at BEFORE UPDATE ON frames
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_statistics_updated_at BEFORE UPDATE ON statistics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();