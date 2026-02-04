from django.db import models
import uuid

class Audio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='audio_files/')
    code_image = models.URLField(blank=True, null=True, help_text="Supabase URL of the generated waveform code image")
    cloudinary_audio_url = models.URLField(blank=True, null=True, help_text="Cloudinary URL of the audio file")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.id})"
