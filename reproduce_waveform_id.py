import os
import json
import numpy as np
import uuid
from PIL import Image, ImageDraw, ImageFont

# Define function from working_audio_api.py (simplified for test)
def create_spotify_waveform_image(waveform_data, scan_id="TEST-ID-123"):
    """Create the Spotify-style waveform code image with vertical bars and ID text"""
    width = 800
    height = 240  # Increased height to accommodate text
    bar_count = len(waveform_data)
    bar_width = 8
    bar_spacing = 4
    max_bar_height = height - 80  # Leave room for text and margins
    
    # Create white background (Spotify style)
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Calculate total width needed for bars
    total_bars_width = bar_count * (bar_width + bar_spacing) - bar_spacing
    start_x = (width - total_bars_width) // 2
    
    # Draw waveform bars (vertical bars like Spotify codes)
    for i, amplitude in enumerate(waveform_data):
        # Calculate bar height based on amplitude
        bar_height = max(4, int(amplitude * max_bar_height))
        
        # Center the bar vertically (but shifted up slightly due to text at bottom)
        # Center within the "waveform area" (top 160px)
        waveform_area_height = height - 60
        y_start = (waveform_area_height - bar_height) // 2
        y_end = y_start + bar_height
        
        # Calculate x position
        x_start = start_x + i * (bar_width + bar_spacing)
        x_end = x_start + bar_width
        
        # Draw rounded rectangle for each bar (Spotify style)
        corner_radius = min(bar_width // 2, (y_end - y_start) // 2)
        if corner_radius <= 0:
            draw.rectangle([x_start, y_start, x_end, y_end], fill='black')
        else:
            draw.rounded_rectangle([x_start, y_start, x_end, y_end], radius=corner_radius, fill='black')
    
    # Draw ID text at the bottom
    try:
        # Use a default font, size 40
        try:
             # Try to load a nice font if available (Linux standard paths)
            font_paths = [
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                 "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            ]
            font = None
            for path in font_paths:
                if os.path.exists(path):
                    font = ImageFont.truetype(path, 40)
                    break
            if not font:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
            
        text = str(scan_id)
        # Calculate text position to center it
        try:
            # Pillow >= 10.0.0
            left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
            text_width = right - left
        except AttributeError:
            # Older Pillow versions
            text_width, text_height = draw.textsize(text, font=font)
            
        text_x = (width - text_width) // 2
        text_y = height - 50  # Position near bottom
        
        draw.text((text_x, text_y), text, fill='black', font=font)
    except Exception as e:
        print(f"⚠️ Error drawing text: {e}")
    
    return image

# Generate dummy waveform data
bar_count = 60
x = np.linspace(0, 4 * np.pi, bar_count)
waveform_data = np.abs(np.sin(x)) * 0.8 + 0.1

# Generate image
scan_id = "1DJF456FHFB7834"
print(f"Generating waveform for ID: {scan_id}")
image = create_spotify_waveform_image(waveform_data, scan_id)

filename = "test_visual_id.png"
image.save(filename)
print(f"Saved to {filename}")
print(f"Image size: {image.size}")
