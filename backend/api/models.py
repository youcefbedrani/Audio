"""
Models for the Audio Art Frame API.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import qrcode
import io
from django.core.files.base import ContentFile
from cloudinary_storage.storage import MediaCloudinaryStorage


class Frame(models.Model):
    """Model representing a physical art frame."""
    
    FRAME_TYPES = [
        ('wooden', 'Wooden Frame'),
        ('metal', 'Metal Frame'),
        ('plastic', 'Plastic Frame'),
        ('glass', 'Glass Frame'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    frame_type = models.CharField(max_length=20, choices=FRAME_TYPES, default='wooden')
    image = models.ImageField(upload_to='frames/', storage=MediaCloudinaryStorage())
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True, storage=MediaCloudinaryStorage())
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='frames')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_available = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def generate_qr_code(self):
        """Generate QR code for this frame."""
        if not self.qr_code:
            # Create QR code data
            qr_data = f"audio_frame://frame/{self.id}"
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save to buffer
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            # Save to model
            self.qr_code.save(
                f'qr_frame_{self.id}.png',
                ContentFile(buffer.getvalue()),
                save=True
            )
        
        return self.qr_code.url


class Order(models.Model):
    """Model representing an order for a frame."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHODS = [
        ('COD', 'Cash on Delivery'),
        ('online', 'Online Payment'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE, related_name='orders')
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True)
    delivery_address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    wilaya = models.CharField(max_length=100, blank=True)  # Algerian wilaya
    baladya = models.CharField(max_length=100, blank=True)  # Algerian baladya
    audio_file = models.FileField(upload_to='order_audio/', blank=True, null=True, storage=MediaCloudinaryStorage())
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='COD')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class Statistic(models.Model):
    """Model for tracking frame statistics."""
    
    frame = models.OneToOneField(Frame, on_delete=models.CASCADE, related_name='statistics')
    scans_count = models.PositiveIntegerField(default=0)
    plays_count = models.PositiveIntegerField(default=0)
    last_scan = models.DateTimeField(null=True, blank=True)
    last_play = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Stats for {self.frame.title}"
    
    def increment_scan(self):
        """Increment scan count and update last scan time."""
        self.scans_count += 1
        self.last_scan = timezone.now()
        self.save()
    
    def increment_play(self):
        """Increment play count and update last play time."""
        self.plays_count += 1
        self.last_play = timezone.now()
        self.save()


class AudioUpload(models.Model):
    """Model for tracking audio uploads."""
    
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE, related_name='audio_uploads')
    audio_file = models.FileField(upload_to='audio/', storage=MediaCloudinaryStorage())
    duration = models.FloatField(help_text="Duration in seconds")
    file_size = models.PositiveIntegerField(help_text="File size in bytes")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"Audio for {self.frame.title} - {self.uploaded_at}"
