from PIL import Image, ImageDraw, ImageFont
import os

def create_mock_scan_id_image(scan_id, filename="mock_scan.png"):
    # Create a white image (simulating a frame/screen)
    img = Image.new('RGB', (800, 400), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw some random "waveform" lines at the top
    for i in range(10, 200, 10):
        h = (i * 7) % 150
        draw.rectangle([i*4, 150-h, i*4+5, 150+h], fill=(0, 0, 0))
    
    # Draw the Scan ID at the bottom (OCR area is bottom 50%)
    # Use a large, clear font
    try:
        # Try to find a common font
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    text = scan_id
    draw.text((200, 300), text, fill=(0, 0, 0), font=font)
    
    img.save(filename)
    print(f"✅ Created mock image: {filename} with ID: {scan_id}")

if __name__ == "__main__":
    # Use one of the IDs from orders_persistence.json
    create_mock_scan_id_image("3E9846696CDD47A", "/home/badran/Downloads/Freelance_2025/audio_frame_art/mock_scan.png")
