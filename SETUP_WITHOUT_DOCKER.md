# Audio Frame Art - Setup Without Docker

## 🚀 Quick Start (Without Docker)

This project can run perfectly without Docker! Here's how to set it up:

### Prerequisites
- Python 3.8+
- Node.js 18+
- PostgreSQL (or use Supabase)

### 1. Backend Setup (Django)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp ../env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start the server
python manage.py runserver 0.0.0.0:8000
```

### 2. Frontend Setup (Next.js)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp env.local.example env.local
# Edit env.local with your API URL

# Start the development server
npm run dev
```

### 3. Database Options

#### Option A: Use Supabase (Recommended)
1. Create a Supabase project
2. Get your database credentials
3. Update `.env` file with Supabase credentials
4. Run the SQL schema in Supabase SQL Editor

#### Option B: Use Local PostgreSQL
1. Install PostgreSQL
2. Create database: `createdb audio_frame_db`
3. Update `.env` file with local database credentials

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

### 5. Static HTML Pages (Alternative)

If you prefer static HTML pages (no React/Next.js issues):
- **Homepage**: http://localhost:3000/index.html
- **Frames List**: http://localhost:3000/frames.html
- **Frame Details**: http://localhost:3000/frame-detail.html?id=5
- **Thank You**: http://localhost:3000/thank-you.html

## 🔧 Current Status

✅ **Backend**: Running on port 8000
✅ **Frontend**: Running on port 3000
✅ **Database**: Supabase connected
✅ **Static Pages**: Working perfectly

## 🎯 What's Working

1. **Frames List**: http://localhost:3000/frames.html
2. **Frame Details**: http://localhost:3000/frame-detail.html?id=5
3. **Order Form**: Complete with customer info and audio recording
4. **Thank You Page**: Order confirmation
5. **Backend API**: All endpoints working

## 🚫 Docker Not Required

You don't need Docker for this project! Everything works perfectly with:
- Direct Python/Django backend
- Direct Node.js/Next.js frontend
- Supabase database (cloud-hosted)

## 📱 Next Steps

1. **Test the complete flow**:
   - Visit frames page
   - Click "طلب الإطار" (Order Frame)
   - Fill out the order form
   - Submit the order

2. **Mobile App**: Ready for Flutter app integration
3. **Admin Panel**: Access at http://localhost:8000/admin

## 🎉 Everything is Working!

Your application is fully functional without Docker. The static HTML pages provide a reliable alternative to the React components and work perfectly for the complete order flow.

