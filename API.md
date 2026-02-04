# Audio Art Frame - API Documentation

Complete API documentation for the Audio Art Frame backend.

## Base URL

```
Production: https://yourdomain.com/api
Development: http://localhost:8000/api
```

## Authentication

The API uses JWT (JSON Web Token) authentication for protected endpoints.

### Getting a Token

```http
POST /api/auth/token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Using the Token

Include the token in the Authorization header:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Refreshing a Token

```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "your_refresh_token"
}
```

## Endpoints

### Frames

#### List All Frames

```http
GET /api/frames/
```

**Response:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Beautiful Wooden Frame",
      "description": "A stunning wooden frame perfect for any photo",
      "frame_type": "wooden",
      "image": "https://res.cloudinary.com/your-cloud/image/upload/v1234567890/frame1.jpg",
      "qr_code": "https://res.cloudinary.com/your-cloud/image/upload/v1234567890/qr_frame_1.png",
      "audio_file": "https://res.cloudinary.com/your-cloud/video/upload/v1234567890/audio1.webm",
      "owner": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com"
      },
      "price": "29.99",
      "is_available": true,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "statistics": {
        "scans_count": 15,
        "plays_count": 12,
        "last_scan": "2024-01-20T14:30:00Z",
        "last_play": "2024-01-20T14:32:00Z"
      }
    }
  ]
}
```

#### Get Frame Details

```http
GET /api/frames/{id}/
```

**Response:**
```json
{
  "id": 1,
  "title": "Beautiful Wooden Frame",
  "description": "A stunning wooden frame perfect for any photo",
  "frame_type": "wooden",
  "image": "https://res.cloudinary.com/your-cloud/image/upload/v1234567890/frame1.jpg",
  "qr_code": "https://res.cloudinary.com/your-cloud/image/upload/v1234567890/qr_frame_1.png",
  "audio_file": "https://res.cloudinary.com/your-cloud/video/upload/v1234567890/audio1.webm",
  "owner": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  },
  "price": "29.99",
  "is_available": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "statistics": {
    "scans_count": 15,
    "plays_count": 12,
    "last_scan": "2024-01-20T14:30:00Z",
    "last_play": "2024-01-20T14:32:00Z"
  }
}
```

#### Create Frame (Authenticated)

```http
POST /api/frames/
Authorization: Bearer your_token
Content-Type: multipart/form-data

{
  "title": "New Frame",
  "description": "Frame description",
  "frame_type": "wooden",
  "image": <file>,
  "audio_file": <file>,
  "price": "25.00",
  "is_available": true
}
```

**Response:**
```json
{
  "id": 2,
  "title": "New Frame",
  "description": "Frame description",
  "frame_type": "wooden",
  "image": "https://res.cloudinary.com/your-cloud/image/upload/v1234567890/frame2.jpg",
  "qr_code": "https://res.cloudinary.com/your-cloud/image/upload/v1234567890/qr_frame_2.png",
  "audio_file": "https://res.cloudinary.com/your-cloud/video/upload/v1234567890/audio2.webm",
  "owner": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  },
  "price": "25.00",
  "is_available": true,
  "created_at": "2024-01-20T15:00:00Z",
  "updated_at": "2024-01-20T15:00:00Z",
  "statistics": {
    "scans_count": 0,
    "plays_count": 0,
    "last_scan": null,
    "last_play": null
  }
}
```

#### Update Frame (Owner Only)

```http
PUT /api/frames/{id}/
Authorization: Bearer your_token
Content-Type: application/json

{
  "title": "Updated Frame Title",
  "description": "Updated description",
  "price": "30.00"
}
```

#### Delete Frame (Owner Only)

```http
DELETE /api/frames/{id}/
Authorization: Bearer your_token
```

### Orders

#### List User Orders

```http
GET /api/orders/user/
Authorization: Bearer your_token
```

**Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 1,
      "frame": {
        "id": 1,
        "title": "Beautiful Wooden Frame",
        "frame_type": "wooden",
        "price": "29.99"
      },
      "customer_name": "John Doe",
      "customer_phone": "+1234567890",
      "customer_email": "john@example.com",
      "delivery_address": "123 Main St, Apt 4B",
      "city": "New York",
      "postal_code": "10001",
      "status": "pending",
      "payment_method": "COD",
      "total_amount": "29.99",
      "notes": "Please deliver after 5 PM",
      "created_at": "2024-01-20T10:00:00Z",
      "updated_at": "2024-01-20T10:00:00Z"
    }
  ]
}
```

#### Create Order

```http
POST /api/order/
Content-Type: application/json

{
  "frame": 1,
  "customer_name": "John Doe",
  "customer_phone": "+1234567890",
  "customer_email": "john@example.com",
  "delivery_address": "123 Main St, Apt 4B",
  "city": "New York",
  "postal_code": "10001",
  "payment_method": "COD",
  "notes": "Please deliver after 5 PM"
}
```

**Response:**
```json
{
  "id": 1,
  "user": null,
  "frame": {
    "id": 1,
    "title": "Beautiful Wooden Frame",
    "frame_type": "wooden",
    "price": "29.99"
  },
  "customer_name": "John Doe",
  "customer_phone": "+1234567890",
  "customer_email": "john@example.com",
  "delivery_address": "123 Main St, Apt 4B",
  "city": "New York",
  "postal_code": "10001",
  "status": "pending",
  "payment_method": "COD",
  "total_amount": "29.99",
  "notes": "Please deliver after 5 PM",
  "created_at": "2024-01-20T10:00:00Z",
  "updated_at": "2024-01-20T10:00:00Z"
}
```

#### Get Order Details

```http
GET /api/order/{id}/
Authorization: Bearer your_token
```

#### Update Order Status (Admin)

```http
PATCH /api/order/{id}/
Authorization: Bearer your_token
Content-Type: application/json

{
  "status": "confirmed"
}
```

### Scanning & Analytics

#### Scan Frame QR Code

```http
GET /api/scan/{frame_id}/
```

**Response:**
```json
{
  "frame_id": 1,
  "frame_title": "Beautiful Wooden Frame",
  "audio_url": "https://res.cloudinary.com/your-cloud/video/upload/v1234567890/audio1.webm",
  "signed_audio_url": "https://res.cloudinary.com/your-cloud/video/upload/s--abc123--/v1234567890/audio1.webm",
  "message": "Audio file found successfully"
}
```

#### Track Audio Play

```http
POST /api/track-play/{frame_id}/
```

**Response:**
```json
{
  "message": "Play tracked successfully",
  "plays_count": 13
}
```

### Admin Statistics

#### Get Admin Statistics

```http
GET /api/stats/
Authorization: Bearer your_token
```

**Response:**
```json
{
  "total_orders": 25,
  "total_frames": 10,
  "total_scans": 150,
  "total_plays": 120,
  "pending_orders": 5,
  "delivered_orders": 15,
  "recent_orders": [
    {
      "id": 1,
      "customer_name": "John Doe",
      "frame": {
        "id": 1,
        "title": "Beautiful Wooden Frame"
      },
      "status": "pending",
      "total_amount": "29.99",
      "created_at": "2024-01-20T10:00:00Z"
    }
  ],
  "top_frames": [
    {
      "id": 1,
      "frame": {
        "id": 1,
        "title": "Beautiful Wooden Frame"
      },
      "scans_count": 15,
      "plays_count": 12,
      "last_scan": "2024-01-20T14:30:00Z",
      "last_play": "2024-01-20T14:32:00Z"
    }
  ]
}
```

## Error Responses

### 400 Bad Request

```json
{
  "field_name": ["This field is required."]
}
```

### 401 Unauthorized

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden

```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found

```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error

```json
{
  "detail": "A server error occurred."
}
```

## Rate Limiting

- API endpoints: 10 requests per second
- Web endpoints: 30 requests per second
- Burst allowance: 20 requests for API, 50 for web

## CORS

The API supports CORS for the following origins:
- `http://localhost:3000` (development)
- `https://yourdomain.com` (production)

## File Upload

### Supported Formats

**Images:**
- JPEG, PNG, WebP
- Maximum size: 10MB

**Audio:**
- MP3, WAV, WebM, OGG
- Maximum size: 50MB
- Maximum duration: 5 minutes

### Upload Process

1. Use `multipart/form-data` content type
2. Include file in form data
3. Server uploads to Cloudinary
4. Returns public URL

## Webhooks (Future Feature)

Planned webhook endpoints for order status updates:

```http
POST /api/webhooks/order-status/
Content-Type: application/json

{
  "order_id": 1,
  "status": "delivered",
  "timestamp": "2024-01-20T15:00:00Z"
}
```

## SDKs

### JavaScript/TypeScript

```typescript
import { framesApi, ordersApi } from './lib/api';

// Get all frames
const frames = await framesApi.getAll();

// Create order
const order = await ordersApi.create({
  frame: 1,
  customer_name: 'John Doe',
  customer_phone: '+1234567890',
  delivery_address: '123 Main St',
  city: 'New York',
  postal_code: '10001'
});
```

### Python

```python
import requests

# Get frames
response = requests.get('http://localhost:8000/api/frames/')
frames = response.json()

# Create order
order_data = {
    'frame': 1,
    'customer_name': 'John Doe',
    'customer_phone': '+1234567890',
    'delivery_address': '123 Main St',
    'city': 'New York',
    'postal_code': '10001'
}
response = requests.post('http://localhost:8000/api/order/', json=order_data)
order = response.json()
```

## Testing

### Postman Collection

Import the provided Postman collection for easy API testing:

1. Download `Audio_Art_Frame_API.postman_collection.json`
2. Import into Postman
3. Set environment variables for base URL and tokens
4. Run tests

### cURL Examples

```bash
# Get all frames
curl -X GET http://localhost:8000/api/frames/

# Create order
curl -X POST http://localhost:8000/api/order/ \
  -H "Content-Type: application/json" \
  -d '{
    "frame": 1,
    "customer_name": "John Doe",
    "customer_phone": "+1234567890",
    "delivery_address": "123 Main St",
    "city": "New York",
    "postal_code": "10001"
  }'

# Scan frame
curl -X GET http://localhost:8000/api/scan/1/
```

## Changelog

### v1.0.0 (2024-01-20)
- Initial API release
- Frame management endpoints
- Order processing
- QR code scanning
- Audio playback tracking
- Admin statistics
- JWT authentication
