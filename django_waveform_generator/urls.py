"""
URL configuration for audio waveform generation
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AudioViewSet

router = DefaultRouter()
router.register(r'audio', AudioViewSet, basename='audio')

urlpatterns = [
    path('api/', include(router.urls)),
]
