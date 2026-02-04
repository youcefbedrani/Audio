#!/bin/bash
# Start the Supabase Docker API with Spotify Waveform Code Generation

echo "🚀 Starting Supabase Docker API..."
echo "📦 Make sure 'wave_codes' bucket exists in Supabase Storage!"

# Install dependencies if needed
if ! python3 -c "import supabase" 2>/dev/null; then
    echo "📥 Installing supabase library..."
    pip3 install supabase
fi

# Start the server
python3 supabase_docker_api.py

