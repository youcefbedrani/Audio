"""
Admin configuration for the API app.
"""
from django.contrib import admin
from .models import Frame, Order, Statistic, AudioUpload


@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin):
    """Admin interface for Frame model."""
    
    list_display = ['title', 'frame_type', 'price', 'is_available', 'owner', 'created_at']
    list_filter = ['frame_type', 'is_available', 'created_at']
    search_fields = ['title', 'description', 'owner__username']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'frame_type', 'price', 'is_available')
        }),
        ('Media', {
            'fields': ('image', 'audio_file', 'waveform_image')
        }),
        ('Owner', {
            'fields': ('owner',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model."""
    
    list_display = [
        'id', 'customer_name', 'customer_phone', 'frame', 'status', 
        'payment_method', 'total_amount', 'created_at'
    ]
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['customer_name', 'customer_phone', 'customer_email', 'frame__title']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'frame', 'status', 'payment_method', 'total_amount')
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'customer_phone', 'customer_email')
        }),
        ('Delivery Information', {
            'fields': ('delivery_address', 'city', 'postal_code')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    """Admin interface for Statistic model."""
    
    list_display = [
        'frame', 'scans_count', 'plays_count', 'last_scan', 'last_play'
    ]
    list_filter = ['created_at', 'updated_at']
    search_fields = ['frame__title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(AudioUpload)
class AudioUploadAdmin(admin.ModelAdmin):
    """Admin interface for AudioUpload model."""
    
    list_display = ['frame', 'duration', 'file_size', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['frame__title']
    readonly_fields = ['uploaded_at']
