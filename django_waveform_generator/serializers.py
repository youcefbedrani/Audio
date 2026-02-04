"""
Django REST Framework serializers for audio waveform generation
"""

from rest_framework import serializers
from .models import Audio

class AudioSerializer(serializers.ModelSerializer):
    """Serializer for Audio model with waveform code support."""
    
    has_waveform_code = serializers.ReadOnlyField()
    waveform_code_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Audio
        fields = [
            'id', 'title', 'audio_file', 'audio_url', 'code_image',
            'has_waveform_code', 'waveform_code_url', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'code_image', 'created_at', 'updated_at']
    
    def get_waveform_code_url(self, obj):
        """Get the waveform code image URL."""
        return obj.get_waveform_code_url()

class AudioUploadSerializer(serializers.ModelSerializer):
    """Serializer for audio file upload with automatic waveform generation."""
    
    class Meta:
        model = Audio
        fields = ['title', 'audio_file', 'audio_url']
    
    def create(self, validated_data):
        """Create audio instance and generate waveform code."""
        # The waveform generation will be handled in the viewset
        return super().create(validated_data)

class WaveformRegenerateSerializer(serializers.Serializer):
    """Serializer for regenerating waveform codes."""
    
    force_regenerate = serializers.BooleanField(
        default=False,
        help_text="Force regeneration even if waveform code already exists"
    )
