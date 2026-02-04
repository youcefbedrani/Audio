"""
URL configuration for the API app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

urlpatterns = [
    # Frame endpoints
    path('frames/', views.FrameListCreateView.as_view(), name='frame-list-create'),
    path('frames/<int:pk>/', views.FrameDetailView.as_view(), name='frame-detail'),
    path('frames/user/', views.UserFramesView.as_view(), name='user-frames'),
    
    # Order endpoints
    path('orders/', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('orders/user/', views.UserOrdersView.as_view(), name='user-orders'),
    
    # Scan and play tracking
    path('scan/<int:frame_id>/', views.scan_frame, name='scan-frame'),
    path('track-play/<int:frame_id>/', views.track_play, name='track-play'),
    path('compare-waveform/', views.compare_waveform_image, name='compare-waveform'),
    
    # Audio upload
    path('frames/<int:frame_id>/upload-audio/', views.AudioUploadView.as_view(), name='upload-audio'),
    
    # Admin endpoints
    path('stats/', views.AdminStatsView.as_view(), name='admin-stats'),
]
