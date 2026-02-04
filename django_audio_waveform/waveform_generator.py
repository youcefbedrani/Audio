import numpy as np
from PIL import Image, ImageDraw
import io
import hashlib

class SpotifyWaveformGenerator:
    """
    Generates Spotify-style waveform code images from audio files.
    The waveform pattern is reproducible based on the audio file's unique ID.
    """
    
    def __init__(self, width=800, height=200, bar_width=2, bar_spacing=1):
        self.width = width
        self.height = height
        self.bar_width = bar_width
        self.bar_spacing = bar_spacing
        self.max_bars = (width - bar_width) // (bar_width + bar_spacing)
    
    def generate_waveform_from_audio(self, audio_file_path, audio_id):
        """
        Generate a reproducible waveform pattern based on the audio file and ID.
        """
        # Use the audio ID as a seed for reproducible patterns
        seed = self._generate_seed_from_id(audio_id)
        np.random.seed(seed)
        
        # Generate waveform data (simulated - in production, you'd analyze actual audio)
        waveform_data = self._generate_waveform_data()
        
        # Create the image
        image = self._create_waveform_image(waveform_data)
        
        return image
    
    def _generate_seed_from_id(self, audio_id):
        """Generate a consistent seed from the audio ID."""
        # Convert UUID to a consistent integer seed
        id_str = str(audio_id)
        hash_obj = hashlib.md5(id_str.encode())
        return int(hash_obj.hexdigest()[:8], 16)
    
    def _generate_waveform_data(self):
        """Generate waveform bar heights that look like a Spotify code."""
        # Create a pattern that looks like a real audio waveform
        # with varying intensities and some structure
        
        # Generate base pattern with some structure
        base_pattern = np.random.normal(0.3, 0.2, self.max_bars)
        base_pattern = np.clip(base_pattern, 0, 1)
        
        # Add some "beats" or "peaks" to make it look more realistic
        beat_indices = np.random.choice(self.max_bars, size=self.max_bars // 8, replace=False)
        for idx in beat_indices:
            # Create a peak with surrounding bars
            start = max(0, idx - 2)
            end = min(self.max_bars, idx + 3)
            base_pattern[start:end] = np.maximum(base_pattern[start:end], 
                                               np.random.uniform(0.6, 1.0, end - start))
        
        # Add some variation to make it look more organic
        noise = np.random.normal(0, 0.1, self.max_bars)
        waveform_data = np.clip(base_pattern + noise, 0, 1)
        
        return waveform_data
    
    def _create_waveform_image(self, waveform_data):
        """Create the actual waveform image."""
        # Create a white background
        image = Image.new('RGB', (self.width, self.height), 'white')
        draw = ImageDraw.Draw(image)
        
        # Calculate bar positions
        x_offset = (self.width - (self.max_bars * (self.bar_width + self.bar_spacing) - self.bar_spacing)) // 2
        
        for i, amplitude in enumerate(waveform_data):
            # Calculate bar height (minimum height for visibility)
            bar_height = max(4, int(amplitude * (self.height - 20)))
            
            # Center the bar vertically
            y_start = (self.height - bar_height) // 2
            y_end = y_start + bar_height
            
            # Calculate x position
            x_start = x_offset + i * (self.bar_width + self.bar_spacing)
            x_end = x_start + self.bar_width
            
            # Draw the bar
            draw.rectangle([x_start, y_start, x_end, y_end], fill='black')
        
        return image
    
    def generate_waveform_bytes(self, audio_file_path, audio_id):
        """Generate waveform image and return as bytes."""
        image = self.generate_waveform_from_audio(audio_file_path, audio_id)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return img_byte_arr.getvalue()

# Alternative: Generate waveform from actual audio file (requires librosa)
class RealAudioWaveformGenerator(SpotifyWaveformGenerator):
    """
    Generates waveform from actual audio file analysis.
    Requires librosa: pip install librosa
    """
    
    def generate_waveform_from_audio(self, audio_file_path, audio_id):
        """Generate waveform from actual audio file."""
        try:
            import librosa
            import librosa.display
            
            # Load audio file
            y, sr = librosa.load(audio_file_path)
            
            # Generate waveform data from actual audio
            waveform_data = self._extract_waveform_from_audio(y, sr)
            
            # Create the image
            image = self._create_waveform_image(waveform_data)
            
            return image
            
        except ImportError:
            # Fallback to simulated waveform if librosa is not available
            return super().generate_waveform_from_audio(audio_file_path, audio_id)
    
    def _extract_waveform_from_audio(self, y, sr):
        """Extract waveform data from actual audio."""
        # Downsample to our target number of bars
        hop_length = len(y) // self.max_bars
        
        # Calculate RMS energy for each segment
        waveform_data = []
        for i in range(self.max_bars):
            start = i * hop_length
            end = min((i + 1) * hop_length, len(y))
            segment = y[start:end]
            
            if len(segment) > 0:
                # Calculate RMS energy and normalize
                rms = np.sqrt(np.mean(segment**2))
                normalized_rms = min(1.0, rms * 10)  # Scale for visibility
                waveform_data.append(normalized_rms)
            else:
                waveform_data.append(0.1)  # Minimum height
        
        return np.array(waveform_data)
