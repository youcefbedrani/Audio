from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from django.core.files.base import ContentFile
import cloudinary
import cloudinary.uploader
from supabase import create_client, Client
import os
import tempfile
from .models import Audio
from .serializers import AudioSerializer, AudioUploadSerializer
from .waveform_generator import SpotifyWaveformGenerator

class AudioViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling audio file uploads and waveform generation.
    """
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AudioUploadSerializer
        return AudioSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Handle audio file upload and generate waveform code image.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create the audio instance
        audio = serializer.save()
        
        try:
            # Generate waveform code image
            waveform_generator = SpotifyWaveformGenerator()
            waveform_bytes = waveform_generator.generate_waveform_bytes(
                audio.audio_file.path, 
                str(audio.id)
            )
            
            # Upload audio to Cloudinary
            cloudinary_url = self._upload_to_cloudinary(audio.audio_file.path)
            
            # Upload waveform image to Supabase Storage
            supabase_url = self._upload_to_supabase_storage(
                waveform_bytes, 
                f"waveform_{audio.id}.png"
            )
            
            # Update the audio instance with URLs
            audio.code_image = supabase_url
            audio.cloudinary_audio_url = cloudinary_url
            audio.save()
            
            # Return the created audio with all URLs
            response_serializer = AudioSerializer(audio)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            # If anything fails, delete the created audio instance
            audio.delete()
            return Response(
                {'error': f'Failed to process audio file: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _upload_to_cloudinary(self, file_path):
        """Upload audio file to Cloudinary."""
        try:
            # Configure Cloudinary (you should set these in your Django settings)
            cloudinary.config(
                cloud_name=settings.CLOUDINARY_CLOUD_NAME,
                api_key=settings.CLOUDINARY_API_KEY,
                api_secret=settings.CLOUDINARY_API_SECRET
            )
            
            # Upload the file
            result = cloudinary.uploader.upload(
                file_path,
                folder="audio_frame_art/audio",
                resource_type="video",  # For audio files
                use_filename=True,
                unique_filename=True
            )
            
            return result['secure_url']
            
        except Exception as e:
            print(f"Cloudinary upload error: {e}")
            return None
    
    def _upload_to_supabase_storage(self, file_bytes, filename):
        """Upload waveform image to Supabase Storage."""
        try:
            # Initialize Supabase client
            supabase: Client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_ANON_KEY
            )
            
            # Upload to Supabase Storage
            result = supabase.storage.from_("wave_codes").upload(
                filename,
                file_bytes,
                file_options={"content-type": "image/png"}
            )
            
            if result.get('error'):
                raise Exception(f"Supabase upload error: {result['error']}")
            
            # Get the public URL
            public_url = supabase.storage.from_("wave_codes").get_public_url(filename)
            
            return public_url
            
        except Exception as e:
            print(f"Supabase upload error: {e}")
            return None
    
    @action(detail=True, methods=['post'])
    def regenerate_waveform(self, request, pk=None):
        """
        Regenerate the waveform code image for an existing audio file.
        """
        audio = self.get_object()
        
        try:
            # Generate new waveform
            waveform_generator = SpotifyWaveformGenerator()
            waveform_bytes = waveform_generator.generate_waveform_bytes(
                audio.audio_file.path, 
                str(audio.id)
            )
            
            # Upload to Supabase Storage
            supabase_url = self._upload_to_supabase_storage(
                waveform_bytes, 
                f"waveform_{audio.id}.png"
            )
            
            if supabase_url:
                audio.code_image = supabase_url
                audio.save()
                
                serializer = AudioSerializer(audio)
                return Response(serializer.data)
            else:
                return Response(
                    {'error': 'Failed to upload waveform to Supabase'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        except Exception as e:
            return Response(
                {'error': f'Failed to regenerate waveform: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def waveform_image(self, request, pk=None):
        """
        Get the waveform code image directly.
        """
        audio = self.get_object()
        
        if not audio.code_image:
            return Response(
                {'error': 'No waveform code image available'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response({'image_url': audio.code_image})
