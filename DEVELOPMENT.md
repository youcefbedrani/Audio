# Audio Art Frame - Development Guide

This guide covers setting up the development environment for the Audio Art Frame project.

## Project Structure

```
audio_frame_art/
├── backend/                 # Django REST API
│   ├── core/               # Django project settings
│   ├── api/                # API app with models, views, serializers
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Production Docker image
├── frontend/               # Next.js web application
│   ├── src/
│   │   ├── app/           # Next.js app router pages
│   │   ├── components/    # React components
│   │   └── lib/           # Utilities and API client
│   ├── package.json       # Node.js dependencies
│   └── Dockerfile         # Production Docker image
├── mobile/                 # Flutter mobile app
│   ├── lib/
│   │   ├── models/        # Data models
│   │   ├── services/      # API and audio services
│   │   └── screens/       # App screens
│   └── pubspec.yaml       # Flutter dependencies
├── docker-compose.yml     # Production deployment
├── docker-compose.dev.yml # Development deployment
└── nginx.conf             # Reverse proxy configuration
```

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Flutter 3.0+
- Docker & Docker Compose
- PostgreSQL 15+
- Git

### Option 1: Docker Development (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd audio_frame_art
   ```

2. **Set up environment**
   ```bash
   cp env.example .env
   # Edit .env with your development settings
   ```

3. **Start development environment**
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```

4. **Access applications**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000
   - Admin: http://localhost:8000/admin

### Option 2: Local Development

#### Backend Setup

1. **Create virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up database**
   ```bash
   # Start PostgreSQL (if not using Docker)
   sudo systemctl start postgresql
   
   # Create database
   createdb audio_frame_db
   ```

4. **Configure environment**
   ```bash
   cp ../env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

#### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment**
   ```bash
   cp ../env.example .env.local
   # Edit .env.local with your settings
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

#### Mobile Setup

1. **Install Flutter**
   ```bash
   # Follow Flutter installation guide
   # https://docs.flutter.dev/get-started/install
   ```

2. **Install dependencies**
   ```bash
   cd mobile
   flutter pub get
   ```

3. **Configure API URL**
   ```bash
   # Edit lib/services/api_service.dart
   # Update baseUrl to your backend URL
   ```

4. **Run the app**
   ```bash
   flutter run
   ```

## Development Workflow

### Backend Development

1. **Create new models**
   ```bash
   # Add models in api/models.py
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create API endpoints**
   ```bash
   # Add views in api/views.py
   # Add URLs in api/urls.py
   # Add serializers in api/serializers.py
   ```

3. **Test API endpoints**
   ```bash
   # Use Django admin or API testing tools
   python manage.py runserver
   # Visit http://localhost:8000/admin
   ```

### Frontend Development

1. **Create new pages**
   ```bash
   # Add pages in src/app/
   # Use Next.js app router conventions
   ```

2. **Create components**
   ```bash
   # Add components in src/components/
   # Use TypeScript and Tailwind CSS
   ```

3. **Update API client**
   ```bash
   # Modify src/lib/api.ts for new endpoints
   ```

### Mobile Development

1. **Create new screens**
   ```bash
   # Add screens in lib/screens/
   # Follow Flutter conventions
   ```

2. **Update models**
   ```bash
   # Add models in lib/models/
   # Update API service accordingly
   ```

3. **Test on device/emulator**
   ```bash
   flutter run
   ```

## Testing

### Backend Testing

```bash
cd backend
python manage.py test
```

### Frontend Testing

```bash
cd frontend
npm test
```

### Mobile Testing

```bash
cd mobile
flutter test
```

## Code Quality

### Backend

- Use Black for code formatting
- Use flake8 for linting
- Follow Django best practices
- Write docstrings for functions/classes

### Frontend

- Use Prettier for code formatting
- Use ESLint for linting
- Follow React/Next.js best practices
- Use TypeScript for type safety

### Mobile

- Use dart format for code formatting
- Follow Flutter best practices
- Use proper widget composition
- Handle errors gracefully

## Database Management

### Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

### Database Shell

```bash
python manage.py shell
```

### Admin Interface

- Access at http://localhost:8000/admin
- Create superuser: `python manage.py createsuperuser`
- Manage models, users, and permissions

## API Documentation

### Available Endpoints

- `GET /api/frames/` - List all frames
- `POST /api/frames/` - Create new frame
- `GET /api/frames/{id}/` - Get frame details
- `POST /api/order/` - Create new order
- `GET /api/scan/{frame_id}/` - Scan frame QR code
- `POST /api/track-play/{frame_id}/` - Track audio play
- `GET /api/stats/` - Admin statistics

### Authentication

- JWT tokens for API access
- Admin interface uses Django's built-in auth
- Mobile app uses API tokens

## Debugging

### Backend Debugging

1. **Enable debug mode**
   ```python
   DEBUG = True
   ```

2. **Use Django debug toolbar**
   ```bash
   pip install django-debug-toolbar
   ```

3. **Check logs**
   ```bash
   tail -f logs/django.log
   ```

### Frontend Debugging

1. **Browser DevTools**
   - Network tab for API calls
   - Console for JavaScript errors
   - React DevTools extension

2. **Next.js debugging**
   ```bash
   npm run dev
   # Check terminal for errors
   ```

### Mobile Debugging

1. **Flutter Inspector**
   ```bash
   flutter run --debug
   ```

2. **Device logs**
   ```bash
   flutter logs
   ```

## Performance Optimization

### Backend

- Use database indexes
- Implement caching with Redis
- Optimize queries with select_related/prefetch_related
- Use pagination for large datasets

### Frontend

- Use Next.js Image component
- Implement code splitting
- Use React.memo for expensive components
- Optimize bundle size

### Mobile

- Use const constructors
- Implement proper state management
- Optimize image loading
- Use lazy loading for lists

## Deployment

### Development Deployment

```bash
docker-compose -f docker-compose.dev.yml up --build
```

### Production Deployment

```bash
./deploy.sh
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Commit Convention

```
feat: add new feature
fix: fix bug
docs: update documentation
style: code formatting
refactor: code refactoring
test: add tests
chore: maintenance tasks
```

## Troubleshooting

### Common Issues

1. **Port conflicts**
   ```bash
   # Check what's using the port
   lsof -i :8000
   # Kill the process or use different port
   ```

2. **Database connection issues**
   ```bash
   # Check PostgreSQL status
   sudo systemctl status postgresql
   # Check connection
   psql -h localhost -U postgres -d audio_frame_db
   ```

3. **Docker issues**
   ```bash
   # Clean up Docker
   docker system prune -a
   # Rebuild containers
   docker-compose up --build --force-recreate
   ```

4. **Node modules issues**
   ```bash
   # Clear cache and reinstall
   rm -rf node_modules package-lock.json
   npm install
   ```

5. **Flutter issues**
   ```bash
   # Clean and get dependencies
   flutter clean
   flutter pub get
   ```

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Flutter Documentation](https://docs.flutter.dev/)
- [Docker Documentation](https://docs.docker.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
