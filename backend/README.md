# Audio Art Frame - Backend API

Django REST Framework backend for the Audio Art Frame system.

## Features

- **Frame Management**: Create, read, update, delete art frames
- **Order Processing**: Handle customer orders with COD payment
- **QR Code Generation**: Automatic QR code generation for frames
- **Audio Storage**: Cloudinary integration for audio file storage
- **Statistics Tracking**: Track scans and plays for analytics
- **JWT Authentication**: Secure API access
- **Admin Dashboard**: Django admin interface

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Create a `.env` file with:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   DB_NAME=audio_frame_db
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=localhost
   DB_PORT=5432
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   ```

3. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Run Server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Frames
- `GET /api/frames/` - List all available frames
- `POST /api/frames/` - Create a new frame (authenticated)
- `GET /api/frames/{id}/` - Get frame details
- `PUT /api/frames/{id}/` - Update frame (owner only)
- `DELETE /api/frames/{id}/` - Delete frame (owner only)

### Orders
- `GET /api/order/` - List user orders
- `POST /api/order/` - Create new order
- `GET /api/order/{id}/` - Get order details
- `PUT /api/order/{id}/` - Update order status (admin)

### Scanning & Analytics
- `GET /api/scan/{frame_id}/` - Scan QR code and get audio URL
- `POST /api/track-play/{frame_id}/` - Track audio play event
- `GET /api/stats/` - Admin statistics dashboard

### Authentication
- `POST /api/auth/token/` - Get JWT token
- `POST /api/auth/token/refresh/` - Refresh JWT token

## Models

### Frame
- Physical art frame with QR code and audio
- Owner relationship for user management
- Price and availability settings

### Order
- Customer order with delivery information
- Status tracking (pending, confirmed, shipped, delivered)
- COD payment method support

### Statistic
- Track QR code scans and audio plays
- Analytics for frame performance
- Timestamps for last activity

## Cloudinary Integration

- Automatic file upload to Cloudinary
- Signed URLs for secure audio access
- Image optimization for frame photos
- QR code storage in cloud

## Admin Interface

Access Django admin at `/admin/` for:
- Frame management
- Order processing
- User management
- Statistics viewing
- System configuration
