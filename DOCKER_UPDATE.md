# 🐳 Docker Update - Waveform Code Generation

## ✅ What Was Updated:

### 1. **Dockerfile.api**
   - ✅ Added system dependencies for librosa (libsndfile1, ffmpeg)
   - ✅ Changed from `working_audio_api.py` to `supabase_docker_api.py`
   - ✅ Added `/app/uploads/waveforms` directory
   - ✅ Updated environment variables

### 2. **docker-compose.yml**
   - ✅ Updated to use `supabase_docker_api.py`
   - ✅ Added Supabase environment variables
   - ✅ Added Cloudinary environment variables
   - ✅ Added volume mounts for uploads and logs

### 3. **Dependencies**
   - ✅ All required packages already in `requirements-api.txt`:
     - supabase==2.0.0
     - numpy==1.24.3
     - librosa==0.10.1
     - Pillow==10.0.1

## 🚀 How to Build and Run:

### 1. **Build the Docker image:**
   ```bash
   docker-compose build api
   ```

### 2. **Start the container:**
   ```bash
   docker-compose up -d api
   ```

### 3. **Check logs:**
   ```bash
   docker-compose logs -f api
   ```

### 4. **Stop the container:**
   ```bash
   docker-compose down
   ```

## 🔧 Environment Variables:

You can override environment variables in `docker-compose.yml` or create a `.env` file:

```env
CLOUDINARY_API_KEY=your-actual-key
CLOUDINARY_API_SECRET=your-actual-secret
```

## ✅ What Works in Docker:

- ✅ Audio file upload to Cloudinary
- ✅ Waveform code generation (Spotify style)
- ✅ Upload to Supabase Storage (`wave_codes` bucket)
- ✅ Database storage of waveform URLs and metadata
- ✅ All API endpoints

## 📋 Important Notes:

1. **Supabase Storage Bucket:**
   - Must create `wave_codes` bucket in Supabase Dashboard
   - Set to PUBLIC

2. **Volume Mounts:**
   - `/app/uploads` - for temporary waveform files
   - `/app/logs` - for application logs

3. **Port:**
   - API accessible on port 8001
   - Frontend can connect to `http://api:8001` (internal Docker network)

## 🧪 Test in Docker:

```bash
# Test health endpoint
curl http://localhost:8001/health/

# Test storage connection
curl http://localhost:8001/api/test-storage/

# Create order with audio (via your frontend or Postman)
```

## 🔍 Troubleshooting:

If waveform codes aren't uploading:
1. Check Docker logs: `docker-compose logs api`
2. Verify `wave_codes` bucket exists in Supabase
3. Check Supabase Storage permissions
4. Verify environment variables are set correctly

