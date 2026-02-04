"""
Django models for audio waveform generation
"""

from django.db import models
import uuid

class Audio(models.Model):
    """
    Audio model with waveform code image support.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='audio_files/')
    audio_url = models.URLField(blank=True, null=True, help_text="Original audio file URL")
    code_image = models.URLField(blank=True, null=True, help_text="Supabase URL of the generated waveform code image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Audio'
        verbose_name_plural = 'Audio Files'
    
    def __str__(self):
        return f"{self.title} ({self.id})"
    
    @property
    def has_waveform_code(self):
        """Check if waveform code image exists."""
        return bool(self.code_image)
    
    def get_waveform_code_url(self):
        """Get the waveform code image URL."""
        return self.code_image or None
