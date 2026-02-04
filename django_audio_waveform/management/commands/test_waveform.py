from django.core.management.base import BaseCommand
from django_audio_waveform.models import Audio
from django_audio_waveform.waveform_generator import SpotifyWaveformGenerator
import os
import tempfile

class Command(BaseCommand):
    help = 'Test waveform generation for existing audio files'

    def add_arguments(self, parser):
        parser.add_argument('--audio-id', type=str, help='Specific audio ID to test')
        parser.add_argument('--regenerate', action='store_true', help='Regenerate existing waveforms')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing waveform generation...'))
        
        # Get audio files to test
        if options['audio_id']:
            try:
                audios = [Audio.objects.get(id=options['audio_id'])]
            except Audio.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Audio with ID {options["audio_id"]} not found'))
                return
        else:
            audios = Audio.objects.all()[:5]  # Test first 5 audio files
        
        if not audios:
            self.stdout.write(self.style.WARNING('No audio files found'))
            return
        
        generator = SpotifyWaveformGenerator()
        
        for audio in audios:
            self.stdout.write(f'Processing: {audio.title} ({audio.id})')
            
            try:
                # Generate waveform
                waveform_bytes = generator.generate_waveform_bytes(
                    audio.audio_file.path, 
                    str(audio.id)
                )
                
                # Save test image locally
                test_path = f'test_waveform_{audio.id}.png'
                with open(test_path, 'wb') as f:
                    f.write(waveform_bytes)
                
                self.stdout.write(self.style.SUCCESS(f'✅ Generated: {test_path}'))
                
                # Show file size
                size_kb = len(waveform_bytes) / 1024
                self.stdout.write(f'   Size: {size_kb:.1f} KB')
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS('Waveform generation test completed!'))
