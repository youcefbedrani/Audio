#!/usr/bin/env python3
"""
Django Integration Example for Audio Waveform Generator
Shows how to integrate with your existing Django API
"""

# Example Django view integration
def example_django_view():
    """
    Example of how to integrate waveform generation into your Django views
    """
    
    django_view_code = '''
# In your Django views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.conf import settings
import logging
from .models import Audio  # Your existing Audio model
from .waveform_service import generate_waveform_code

logger = logging.getLogger(__name__)

class AudioViewSet(viewsets.ModelViewSet):
    """
    Your existing Audio ViewSet with waveform generation added
    """
    
    def create(self, request, *args, **kwargs):
        """
        Handle audio file upload and automatically generate waveform code.
        """
        # Your existing audio creation logic
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create the audio instance
        audio = serializer.save()
        
        # NEW: Generate waveform code if audio_url is provided
        if hasattr(audio, 'audio_url') and audio.audio_url:
            try:
                waveform_url = generate_waveform_code(
                    audio_url=audio.audio_url,
                    output_name=f"waveform_{audio.id}"
                )
                
                # Save the waveform URL to your model
                audio.code_image = waveform_url
                audio.save()
                
                logger.info(f"Generated waveform code for audio {audio.id}: {waveform_url}")
                
            except Exception as e:
                logger.error(f"Failed to generate waveform for audio {audio.id}: {str(e)}")
                # Don't fail the request, just log the error
        
        # Return response with waveform URL included
        response_serializer = self.get_serializer(audio)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def regenerate_waveform(self, request, pk=None):
        """
        Regenerate waveform code for existing audio.
        """
        audio = self.get_object()
        
        if not hasattr(audio, 'audio_url') or not audio.audio_url:
            return Response(
                {'error': 'No audio URL available for waveform generation'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            waveform_url = generate_waveform_code(
                audio_url=audio.audio_url,
                output_name=f"waveform_{audio.id}"
            )
            
            audio.code_image = waveform_url
            audio.save()
            
            return Response({
                'message': 'Waveform code regenerated successfully',
                'waveform_url': waveform_url
            })
            
        except Exception as e:
            logger.error(f"Failed to regenerate waveform for audio {audio.id}: {str(e)}")
            return Response(
                {'error': f'Failed to regenerate waveform: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
'''
    
    print("Django View Integration Example:")
    print("=" * 40)
    print(django_view_code)

def example_model_integration():
    """
    Example of how to add waveform fields to your existing Audio model
    """
    
    model_code = '''
# In your models.py

from django.db import models
import uuid

class Audio(models.Model):
    """
    Your existing Audio model with waveform code fields added
    """
    # Your existing fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='audio_files/')
    audio_url = models.URLField(blank=True, null=True)  # Add this if not exists
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # NEW: Waveform code fields
    code_image = models.URLField(
        blank=True, 
        null=True, 
        help_text="Supabase URL of the generated waveform code image"
    )
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.id})"
    
    @property
    def has_waveform_code(self):
        """Check if waveform code image exists."""
        return bool(self.code_image)
    
    def get_waveform_code_url(self):
        """Get the waveform code image URL."""
        return self.code_image or None
'''
    
    print("\nDjango Model Integration Example:")
    print("=" * 40)
    print(model_code)

def example_serializer_integration():
    """
    Example of how to add waveform fields to your serializers
    """
    
    serializer_code = '''
# In your serializers.py

from rest_framework import serializers
from .models import Audio

class AudioSerializer(serializers.ModelSerializer):
    """Your existing Audio serializer with waveform fields added"""
    
    # NEW: Add waveform-related fields
    has_waveform_code = serializers.ReadOnlyField()
    waveform_code_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Audio
        fields = [
            'id', 'title', 'audio_file', 'audio_url', 
            'code_image',  # NEW
            'has_waveform_code',  # NEW
            'waveform_code_url',  # NEW
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'code_image', 'created_at', 'updated_at']
    
    def get_waveform_code_url(self, obj):
        """Get the waveform code image URL."""
        return obj.get_waveform_code_url()
'''
    
    print("\nDjango Serializer Integration Example:")
    print("=" * 40)
    print(serializer_code)

def example_api_usage():
    """
    Example of how to use the API
    """
    
    api_examples = '''
# API Usage Examples

# 1. Upload audio with waveform generation
curl -X POST http://localhost:8000/api/audio/ \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer YOUR_TOKEN" \\
  -d '{
    "title": "My Audio Track",
    "audio_url": "https://example.com/audio.mp3"
  }'

# Response will include:
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "My Audio Track",
  "audio_file": null,
  "audio_url": "https://example.com/audio.mp3",
  "code_image": "https://supabase.co/storage/wave_codes/waveform_123e4567.png",
  "has_waveform_code": true,
  "waveform_code_url": "https://supabase.co/storage/wave_codes/waveform_123e4567.png",
  "created_at": "2023-12-01T10:00:00Z",
  "updated_at": "2023-12-01T10:00:00Z"
}

# 2. Regenerate waveform for existing audio
curl -X POST http://localhost:8000/api/audio/123e4567-e89b-12d3-a456-426614174000/regenerate_waveform/ \\
  -H "Authorization: Bearer YOUR_TOKEN"

# 3. Get waveform image URL
curl http://localhost:8000/api/audio/123e4567-e89b-12d3-a456-426614174000/waveform_image/ \\
  -H "Authorization: Bearer YOUR_TOKEN"
'''
    
    print("\nAPI Usage Examples:")
    print("=" * 30)
    print(api_examples)

def example_flutter_integration():
    """
    Example Flutter integration
    """
    
    flutter_code = '''
// Flutter integration example

import 'package:http/http.dart' as http;
import 'dart:convert';

class AudioWaveformService {
  static const String baseUrl = 'https://your-api.com/api';
  
  // Upload audio and get waveform
  static Future<Map<String, dynamic>> uploadAudioWithWaveform({
    required String title,
    required String audioUrl,
    required String authToken,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/audio/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $authToken',
      },
      body: json.encode({
        'title': title,
        'audio_url': audioUrl,
      }),
    );
    
    if (response.statusCode == 201) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to upload audio: ${response.statusCode}');
    }
  }
  
  // Display waveform widget
  Widget buildWaveformDisplay(String waveformUrl) {
    return Container(
      width: 800,
      height: 200,
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(8),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 4,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(8),
        child: Image.network(
          waveformUrl,
          fit: BoxFit.cover,
          loadingBuilder: (context, child, loadingProgress) {
            if (loadingProgress == null) return child;
            return Center(child: CircularProgressIndicator());
          },
          errorBuilder: (context, error, stackTrace) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.error, color: Colors.red),
                  Text('Failed to load waveform'),
                ],
              ),
            );
          },
        ),
      ),
    );
  }
}
'''
    
    print("\nFlutter Integration Example:")
    print("=" * 40)
    print(flutter_code)

def show_setup_instructions():
    """
    Show setup instructions
    """
    
    setup_instructions = '''
# Setup Instructions

## 1. Install Dependencies
pip install -r django_waveform_generator/requirements.txt

## 2. Add to Django Settings
INSTALLED_APPS = [
    # ... your existing apps
    'rest_framework',
    'django_waveform_generator',
]

# Supabase Configuration
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your-anon-key"

## 3. Add URLs
urlpatterns = [
    # ... your existing URLs
    path('api/', include('django_waveform_generator.urls')),
]

## 4. Run Migrations
python manage.py makemigrations
python manage.py migrate

## 5. Create Supabase Storage Bucket
- Go to Supabase dashboard
- Create bucket named "wave_codes"
- Set to public

## 6. Test the Integration
python standalone_waveform_generator.py
'''
    
    print("\nSetup Instructions:")
    print("=" * 25)
    print(setup_instructions)

if __name__ == "__main__":
    print("Django Audio Waveform Generator - Integration Examples")
    print("=" * 70)
    
    # Show all integration examples
    example_django_view()
    example_model_integration()
    example_serializer_integration()
    example_api_usage()
    example_flutter_integration()
    show_setup_instructions()
    
    print("\n" + "=" * 70)
    print("🎉 Integration examples complete!")
    print("Your Django API is ready for Spotify-style waveform generation!")
    print("=" * 70)
