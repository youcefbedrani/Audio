# Audio Art Frame - Deployment Guide

This guide covers deploying the Audio Art Frame application to a VPS or cloud server.

## Prerequisites

- VPS or cloud server (Ubuntu 20.04+ recommended)
- Domain name (optional, for production)
- SSL certificate (Let's Encrypt recommended)
- Docker and Docker Compose installed

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd audio_frame_art
   ```

2. **Configure environment**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Deploy with Docker**
   ```bash
   ./deploy.sh
   ```

## Manual Deployment

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login to apply Docker group changes
```

### 2. Application Setup

```bash
# Clone repository
git clone <repository-url>
cd audio_frame_art

# Create environment file
cp env.example .env
nano .env  # Edit with your configuration
```

### 3. SSL Certificate Setup

For production, use Let's Encrypt:

```bash
# Install Certbot
sudo apt install certbot

# Generate certificate
sudo certbot certonly --standalone -d yourdomain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/key.pem
sudo chown $USER:$USER ssl/cert.pem ssl/key.pem
```

### 4. Deploy Application

```bash
# Build and start services
docker-compose up --build -d

# Run migrations
docker-compose exec api python manage.py migrate

# Create superuser
docker-compose exec api python manage.py createsuperuser

# Collect static files
docker-compose exec api python manage.py collectstatic --noinput
```

## Environment Configuration

### Required Variables

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=audio_frame_db
DB_USER=postgres
DB_PASSWORD=secure-password

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# JWT
JWT_SECRET_KEY=your-jwt-secret-key

# Frontend
NEXT_PUBLIC_API_URL=https://yourdomain.com
NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME=your-cloud-name
```

### Cloudinary Setup

1. Sign up at [Cloudinary](https://cloudinary.com)
2. Get your cloud name, API key, and API secret
3. Update the environment variables

## Production Optimizations

### 1. Database Backup

```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec -T db pg_dump -U postgres audio_frame_db > backup_$DATE.sql
gzip backup_$DATE.sql
EOF

chmod +x backup.sh

# Schedule daily backups
crontab -e
# Add: 0 2 * * * /path/to/backup.sh
```

### 2. Log Rotation

```bash
# Configure logrotate
sudo nano /etc/logrotate.d/audio-frame

# Add:
/var/lib/docker/containers/*/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 root root
}
```

### 3. Monitoring

```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Monitor Docker containers
docker stats

# Check logs
docker-compose logs -f
```

## Security Considerations

### 1. Firewall Setup

```bash
# Configure UFW
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
```

### 2. Database Security

- Use strong passwords
- Enable SSL connections
- Regular backups
- Monitor access logs

### 3. Application Security

- Keep dependencies updated
- Use HTTPS only
- Implement rate limiting
- Regular security audits

## Scaling

### Horizontal Scaling

For high traffic, consider:

1. **Load Balancer**: Use multiple Nginx instances
2. **Database**: Set up read replicas
3. **CDN**: Use Cloudflare or similar
4. **Caching**: Implement Redis for session storage

### Vertical Scaling

- Increase server resources (CPU, RAM)
- Optimize database queries
- Use SSD storage
- Enable compression

## Troubleshooting

### Common Issues

1. **Services not starting**
   ```bash
   docker-compose logs
   docker-compose ps
   ```

2. **Database connection issues**
   ```bash
   docker-compose exec db psql -U postgres -c "SELECT 1;"
   ```

3. **SSL certificate issues**
   ```bash
   openssl x509 -in ssl/cert.pem -text -noout
   ```

4. **Permission issues**
   ```bash
   sudo chown -R $USER:$USER .
   ```

### Performance Issues

1. **Check resource usage**
   ```bash
   docker stats
   htop
   ```

2. **Database performance**
   ```bash
   docker-compose exec db psql -U postgres -c "SELECT * FROM pg_stat_activity;"
   ```

3. **Application logs**
   ```bash
   docker-compose logs api
   docker-compose logs web
   ```

## Maintenance

### Regular Tasks

1. **Update dependencies**
   ```bash
   docker-compose pull
   docker-compose up --build -d
   ```

2. **Database maintenance**
   ```bash
   docker-compose exec db psql -U postgres -c "VACUUM ANALYZE;"
   ```

3. **Log cleanup**
   ```bash
   docker system prune -f
   ```

### Updates

1. **Application updates**
   ```bash
   git pull
   docker-compose up --build -d
   ```

2. **Database migrations**
   ```bash
   docker-compose exec api python manage.py migrate
   ```

## Support

For issues and questions:

1. Check the logs: `docker-compose logs`
2. Review this documentation
3. Check GitHub issues
4. Contact support

## Backup and Recovery

### Backup Strategy

1. **Database**: Daily automated backups
2. **Media files**: Cloudinary handles this
3. **Configuration**: Version control
4. **SSL certificates**: Regular renewal

### Recovery Process

1. **Restore database**
   ```bash
   docker-compose exec -T db psql -U postgres audio_frame_db < backup.sql
   ```

2. **Restart services**
   ```bash
   docker-compose up -d
   ```

3. **Verify functionality**
   ```bash
   curl -I https://yourdomain.com/health
   ```
