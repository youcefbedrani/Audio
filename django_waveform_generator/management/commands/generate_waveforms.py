"""
Django management command to generate waveform codes for existing audio files
"""

from django.core.management.base import BaseCommand, CommandError
from django_waveform_generator.models import Audio
from django_waveform_generator.waveform_service import generate_waveform_code
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Generate waveform codes for audio files that don\'t have them'

    def add_arguments(self, parser):
        parser.add_argument(
            '--audio-id',
            type=str,
            help='Specific audio ID to process'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force regeneration of existing waveform codes'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help='Maximum number of audio files to process (default: 10)'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🎵 Starting waveform code generation...')
        )
        
        # Get audio files to process
        if options['audio_id']:
            try:
                audios = [Audio.objects.get(id=options['audio_id'])]
            except Audio.DoesNotExist:
                raise CommandError(f'Audio with ID {options["audio_id"]} not found')
        else:
            # Get audio files without waveform codes
            queryset = Audio.objects.filter(audio_url__isnull=False)
            if not options['force']:
                queryset = queryset.filter(code_image__isnull=True)
            
            audios = queryset[:options['limit']]
        
        if not audios:
            self.stdout.write(
                self.style.WARNING('No audio files found to process')
            )
            return
        
        self.stdout.write(f'Processing {len(audios)} audio file(s)...')
        
        success_count = 0
        error_count = 0
        
        for audio in audios:
            self.stdout.write(f'Processing: {audio.title} ({audio.id})')
            
            try:
                # Generate waveform code
                waveform_url = generate_waveform_code(
                    audio.audio_url, 
                    f'waveform_{audio.id}'
                )
                
                # Update the audio instance
                audio.code_image = waveform_url
                audio.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f'  ✅ Generated: {waveform_url}')
                )
                success_count += 1
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ❌ Error: {str(e)}')
                )
                error_count += 1
                logger.error(f'Failed to generate waveform for {audio.id}: {str(e)}')
        
        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(
            self.style.SUCCESS(f'✅ Successfully processed: {success_count}')
        )
        if error_count > 0:
            self.stdout.write(
                self.style.ERROR(f'❌ Errors: {error_count}')
            )
        self.stdout.write('='*50)
