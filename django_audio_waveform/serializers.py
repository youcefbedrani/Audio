from rest_framework import serializers
from .models import Audio

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ['id', 'title', 'audio_file', 'code_image', 'cloudinary_audio_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'code_image', 'cloudinary_audio_url', 'created_at', 'updated_at']

class AudioUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ['title', 'audio_file']
    
    def create(self, validated_data):
        # The waveform generation and upload will be handled in the viewset
        return super().create(validated_data)
