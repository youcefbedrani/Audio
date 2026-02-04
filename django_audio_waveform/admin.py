from django.contrib import admin
from .models import Audio

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'created_at', 'has_code_image', 'has_cloudinary_url']
    list_filter = ['created_at']
    search_fields = ['title', 'id']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    def has_code_image(self, obj):
        return bool(obj.code_image)
    has_code_image.boolean = True
    has_code_image.short_description = 'Has Code Image'
    
    def has_cloudinary_url(self, obj):
        return bool(obj.cloudinary_audio_url)
    has_cloudinary_url.boolean = True
    has_cloudinary_url.short_description = 'Has Cloudinary URL'
