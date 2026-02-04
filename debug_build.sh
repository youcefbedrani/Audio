#!/bin/bash
cd frontend
npm install html5-qrcode --save
cd ..
docker-compose down
docker-compose build web > build_log.txt 2>&1
docker-compose up -d >> build_log.txt 2>&1
docker-compose ps >> build_log.txt 2>&1
