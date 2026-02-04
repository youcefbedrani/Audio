#!/bin/bash

# Create certs directory if it doesn't exist
mkdir -p certs

# Generate Self-Signed SSL Certificate
# This command creates a new private key (nginx.key) and a certificate (nginx.crt) valid for 365 days.
# The subject includes your IP address to reduce warnings slightly (though main warning persists).

IP_ADDRESS=$(curl -s ifconfig.me || hostname -I | awk '{print $1}')

echo "Generating SSL Certificate for IP: $IP_ADDRESS"

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout certs/nginx.key \
  -out certs/nginx.crt \
  -subj "/C=DZ/ST=Algiers/L=Algiers/O=AudioFrameArt/OU=IT/CN=$IP_ADDRESS"

echo "Certificate generated in ./certs/"
ls -l certs
