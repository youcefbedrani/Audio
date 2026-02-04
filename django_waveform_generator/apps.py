"""
Django app configuration for audio waveform generation
"""

from django.apps import AppConfig

class DjangoWaveformGeneratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_waveform_generator'
    verbose_name = 'Audio Waveform Generator'
