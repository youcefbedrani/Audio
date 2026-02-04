from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AudioViewSet

router = DefaultRouter()
router.register(r'audio', AudioViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
