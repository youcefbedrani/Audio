# 🚀 Server Status & Instructions

## Current Status
The updated `supabase_docker_api.py` includes:
- ✅ Spotify waveform code generation
- ✅ Supabase Storage upload functionality  
- ✅ Enhanced error handling and logging
- ✅ Test endpoint: `/api/test-storage/`

## 🛠️ To Start the Server

### Option 1: Use the restart script (Recommended)
```bash
./restart_server.sh
```

### Option 2: Manual start
```bash
# Kill existing servers
fuser -k 8001/tcp 2>/dev/null
pkill -f "python.*api.*8001"

# Start the server
python3 supabase_docker_api.py > api_server.log 2>&1 &
```

## 🧪 Test Endpoints

1. **Health Check:**
   ```bash
   curl http://localhost:8001/health/
   ```

2. **Test Supabase Storage:**
   ```bash
   curl http://localhost:8001/api/test-storage/
   ```
   This will show:
   - If `wave_codes` bucket exists
   - If uploads work
   - Current files in bucket

## 📋 What the Server Does

When you create an order with audio:
1. Uploads audio to Cloudinary
2. Analyzes audio with librosa
3. Generates Spotify-style waveform code (vertical bars)
4. **Uploads waveform to Supabase Storage (`wave_codes` bucket)** ⭐
5. Saves waveform URL in database (`qr_code_url` column)
6. Stores metadata including audio URL (`qr_code_data` column)

## ⚠️ Important Setup

1. **Create `wave_codes` bucket in Supabase:**
   - Go to Supabase Dashboard → Storage
   - Click "Create a new bucket"
   - Name: `wave_codes`
   - Set to **PUBLIC**
   - Click "Create bucket"

2. **Install dependencies:**
   ```bash
   pip3 install supabase numpy librosa websockets
   ```

3. **Database columns (already in your SQL):**
   - `audio_file_url` - Stores Cloudinary audio URL
   - `qr_code_url` - Stores Supabase Storage waveform URL
   - `qr_code_data` - Stores waveform metadata (JSON)

## 📝 View Logs

```bash
# Follow logs in real-time
tail -f api_server.log

# View recent logs
tail -50 api_server.log
```

## 🔍 Troubleshooting

If port 8001 is in use:
```bash
# Find what's using it
sudo lsof -i:8001

# Kill it
sudo fuser -k 8001/tcp
```

If Supabase Storage upload fails:
- Check if bucket exists in Supabase Dashboard
- Verify bucket is set to PUBLIC
- Check logs for specific error messages
- Test with: `curl http://localhost:8001/api/test-storage/`

