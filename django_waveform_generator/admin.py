"""
Django admin configuration for audio waveform generation
"""

from django.contrib import admin
from .models import Audio

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'id', 'has_waveform_code', 'created_at', 
        'audio_file_preview', 'waveform_code_preview'
    ]
    list_filter = ['created_at', 'code_image__isnull']
    search_fields = ['title', 'id']
    readonly_fields = ['id', 'created_at', 'updated_at', 'waveform_code_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'audio_file', 'audio_url')
        }),
        ('Waveform Code', {
            'fields': ('code_image', 'waveform_code_preview'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_waveform_code(self, obj):
        return bool(obj.code_image)
    has_waveform_code.boolean = True
    has_waveform_code.short_description = 'Has Waveform'
    
    def audio_file_preview(self, obj):
        if obj.audio_file:
            return f"📁 {obj.audio_file.name.split('/')[-1]}"
        return "No file"
    audio_file_preview.short_description = 'Audio File'
    
    def waveform_code_preview(self, obj):
        if obj.code_image:
            return f"🎵 Waveform Code Available"
        return "No waveform code"
    waveform_code_preview.short_description = 'Waveform Status'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
