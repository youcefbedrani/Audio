# 🗄️ Supabase Database Setup Guide

## ✅ **Current Status: API Working!**

Your API is now running and connected to Supabase! Here's what you need to do to complete the setup:

## 📋 **Step 1: Create the Database Table**

### **Option A: Using Supabase Dashboard (Recommended)**

1. **Go to your Supabase Dashboard**:
   - Open: https://supabase.com/dashboard/project/qksmfogjdurxgzmlcujb
   - Login with your credentials

2. **Go to SQL Editor**:
   - Click on "SQL Editor" in the left sidebar
   - Click "New Query"

3. **Run this SQL**:
   ```sql
   CREATE TABLE IF NOT EXISTS api_order (
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
       audio_file_url TEXT,
       status TEXT DEFAULT 'pending',
       payment_method TEXT DEFAULT 'COD',
       total_amount DECIMAL(10,2) NOT NULL,
       notes TEXT DEFAULT '',
       created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
       updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
   );
   
   -- Enable Row Level Security
   ALTER TABLE api_order ENABLE ROW LEVEL SECURITY;
   
   -- Allow public access for demo (in production, use proper user-based policies)
   DROP POLICY IF EXISTS "Allow public access to api_order" ON api_order;
   CREATE POLICY "Allow public access to api_order" ON api_order
       FOR ALL USING (true);
   
   -- Create indexes for better performance
   CREATE INDEX IF NOT EXISTS idx_api_order_frame_id ON api_order(frame_id);
   CREATE INDEX IF NOT EXISTS idx_api_order_created_at ON api_order(created_at);
   CREATE INDEX IF NOT EXISTS idx_api_order_status ON api_order(status);
   ```

4. **Click "Run"** to execute the SQL

### **Option B: Using Supabase CLI (Advanced)**

If you have Supabase CLI installed:
```bash
supabase db reset
supabase db push
```

## 🧪 **Step 2: Test Order Creation**

Once the table is created, test order creation:

```bash
# Test order creation
curl -X POST http://localhost:8001/api/orders/ \
  -F "customer_name=Test User Supabase" \
  -F "customer_phone=0555123456" \
  -F "delivery_address=Test Address, Algiers" \
  -F "city=Algiers" \
  -F "wilaya=الجزائر" \
  -F "baladya=الجزائر" \
  -F "frame=1" \
  -F "payment_method=COD"
```

## 📊 **Step 3: Verify Orders in Supabase**

1. **Go to Table Editor**:
   - In your Supabase dashboard
   - Click "Table Editor" in the left sidebar
   - Select "api_order" table
   - You should see your orders there!

## 🌐 **Step 4: Test the Complete System**

### **Test Website**:
- Go to: http://localhost:3000
- Create an order through the website
- Check Supabase dashboard to see the order

### **Test Mobile App**:
```bash
cd mobile
flutter run -d web-server --web-port 8081
```
- Open: http://localhost:8081
- Scan QR codes to play audio

## 🔧 **Current System Status**

- ✅ **API**: Running on http://localhost:8001
- ✅ **Website**: Running on http://localhost:3000
- ✅ **Supabase**: Connected and ready
- ⏳ **Database Table**: Needs to be created (see Step 1)
- ✅ **Order Creation**: Ready to work once table is created

## 🚀 **Quick Commands**

### **Start Everything**:
```bash
docker-compose up -d
```

### **Test API Health**:
```bash
curl http://localhost:8001/health/
```

### **Test Order Creation**:
```bash
curl -X POST http://localhost:8001/api/orders/ \
  -F "customer_name=Your Name" \
  -F "customer_phone=0555123456" \
  -F "delivery_address=Your Address" \
  -F "city=Algiers" \
  -F "wilaya=الجزائر" \
  -F "baladya=الجزائر" \
  -F "frame=1" \
  -F "payment_method=COD"
```

### **View Orders**:
```bash
curl http://localhost:8001/api/orders/
```

## 🎯 **Expected Results**

After completing Step 1 (creating the table):

1. **Orders will be saved to Supabase** ✅
2. **You can see orders in Supabase dashboard** ✅
3. **Website order creation works** ✅
4. **Mobile app QR scanning works** ✅
5. **Audio playback works** ✅

## 🔗 **Important Links**

- **Supabase Dashboard**: https://supabase.com/dashboard/project/qksmfogjdurxgzmlcujb
- **Website**: http://localhost:3000
- **API Health**: http://localhost:8001/health/
- **API Orders**: http://localhost:8001/api/orders/

## ⚠️ **Troubleshooting**

### **If orders aren't saving to Supabase**:
1. Check if the table exists in Supabase dashboard
2. Check API logs: `docker-compose logs api`
3. Verify Supabase connection: `curl http://localhost:8001/health/`

### **If table creation fails**:
1. Make sure you're logged into the correct Supabase project
2. Check if you have the right permissions
3. Try running the SQL in smaller chunks

---

## 🎉 **You're Almost There!**

Just create the database table (Step 1) and your Audio Frame Art system will be fully functional with Supabase integration! 🚀
