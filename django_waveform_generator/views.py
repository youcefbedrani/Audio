"""
Django REST Framework views for audio waveform generation
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import logging

from .models import Audio
from .serializers import AudioSerializer, AudioUploadSerializer, WaveformRegenerateSerializer
from .waveform_service import generate_waveform_code

logger = logging.getLogger(__name__)

class AudioViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling audio file uploads and waveform code generation.
    """
    queryset = Audio.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AudioUploadSerializer
        return AudioSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Handle audio file upload and automatically generate waveform code.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create the audio instance
        audio = serializer.save()
        
        try:
            # Generate waveform code if audio_url is provided
            if audio.audio_url:
                waveform_url = self._generate_waveform_code(audio)
                if waveform_url:
                    audio.code_image = waveform_url
                    audio.save()
                    logger.info(f"Generated waveform code for audio {audio.id}: {waveform_url}")
                else:
                    logger.warning(f"Failed to generate waveform code for audio {audio.id}")
            else:
                logger.info(f"No audio_url provided for audio {audio.id}, skipping waveform generation")
            
            # Return the created audio with all URLs
            response_serializer = AudioSerializer(audio)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error processing audio {audio.id}: {str(e)}")
            # Don't delete the audio instance, just log the error
            response_serializer = AudioSerializer(audio)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def _generate_waveform_code(self, audio):
        """Generate waveform code for an audio instance."""
        try:
            # Use audio ID as the output name for consistency
            output_name = f"waveform_{audio.id}"
            waveform_url = generate_waveform_code(audio.audio_url, output_name)
            return waveform_url
        except Exception as e:
            logger.error(f"Failed to generate waveform code for audio {audio.id}: {str(e)}")
            return None
    
    @action(detail=True, methods=['post'], serializer_class=WaveformRegenerateSerializer)
    def regenerate_waveform(self, request, pk=None):
        """
        Regenerate the waveform code image for an existing audio file.
        """
        audio = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        force_regenerate = serializer.validated_data.get('force_regenerate', False)
        
        # Check if waveform already exists and not forcing regeneration
        if audio.code_image and not force_regenerate:
            return Response({
                'message': 'Waveform code already exists. Use force_regenerate=true to regenerate.',
                'waveform_url': audio.code_image
            }, status=status.HTTP_200_OK)
        
        if not audio.audio_url:
            return Response({
                'error': 'No audio URL available for waveform generation'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Generate new waveform code
            waveform_url = self._generate_waveform_code(audio)
            
            if waveform_url:
                audio.code_image = waveform_url
                audio.save()
                
                response_serializer = AudioSerializer(audio)
                return Response({
                    'message': 'Waveform code regenerated successfully',
                    'audio': response_serializer.data
                })
            else:
                return Response({
                    'error': 'Failed to generate waveform code'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            logger.error(f"Error regenerating waveform for audio {audio.id}: {str(e)}")
            return Response({
                'error': f'Failed to regenerate waveform: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'])
    def waveform_image(self, request, pk=None):
        """
        Get the waveform code image URL for an audio file.
        """
        audio = self.get_object()
        
        if not audio.code_image:
            return Response({
                'error': 'No waveform code image available',
                'message': 'Use regenerate_waveform endpoint to generate one'
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'waveform_url': audio.code_image,
            'audio_id': str(audio.id),
            'audio_title': audio.title
        })
    
    @action(detail=False, methods=['get'])
    def waveform_stats(self, request):
        """
        Get statistics about waveform code generation.
        """
        total_audio = self.get_queryset().count()
        with_waveform = self.get_queryset().filter(code_image__isnull=False).count()
        without_waveform = total_audio - with_waveform
        
        return Response({
            'total_audio_files': total_audio,
            'with_waveform_codes': with_waveform,
            'without_waveform_codes': without_waveform,
            'waveform_generation_rate': round((with_waveform / total_audio * 100) if total_audio > 0 else 0, 2)
        })
