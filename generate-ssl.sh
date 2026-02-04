#!/bin/bash

# Create ssl directory if it doesn't exist
mkdir -p ssl

# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/nginx.key \
  -out ssl/nginx.crt \
  -subj "/C=DZ/ST=Algiers/L=Algiers/O=AudioFrameArt/CN=localhost"

echo "✅ SSL certificates generated in ./ssl directory"
chmod 600 ssl/nginx.key
chmod 644 ssl/nginx.crt
