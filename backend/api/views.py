"""
Views for the Audio Art Frame API.
"""
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
import cv2
import numpy as np
from PIL import Image
import requests
import tempfile
import os
from .models import Frame, Order, Statistic, AudioUpload
from .serializers import (
    FrameSerializer, FrameCreateSerializer, OrderSerializer, OrderCreateSerializer,
    StatisticSerializer, AudioUploadSerializer, ScanResponseSerializer, AdminStatsSerializer
)
import cloudinary
import cloudinary.utils


class FrameListCreateView(generics.ListCreateAPIView):
    """List all frames or create a new frame."""
    
    queryset = Frame.objects.filter(is_available=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FrameCreateSerializer
        return FrameSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FrameDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a frame."""
    
    queryset = Frame.objects.all()
    serializer_class = FrameSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class OrderListCreateView(generics.ListCreateAPIView):
    """List orders or create a new order."""
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]  # Allow public order creation
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer
    
    def get_queryset(self):
        queryset = Order.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        
        # Add filtering and searching
        search_query = self.request.query_params.get('search', None)
        status_filter = self.request.query_params.get('status', None)
        
        if search_query:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(customer_name__icontains=search_query) |
                Q(customer_phone__icontains=search_query) |
                Q(scan_id__icontains=search_query)
            )
            
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset.select_related('user', 'frame').order_by('-created_at', '-id')
    
    def perform_create(self, serializer):
        # For public orders, create a guest user or use a default user
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            # Create or get a guest user for public orders
            guest_user, created = User.objects.get_or_create(
                username='guest',
                defaults={'email': 'guest@example.com'}
            )
            serializer.save(user=guest_user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete an order."""
    
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def scan_frame(request, frame_id):
    """
    Handle QR code scan and return audio URL.
    Increments scan count and returns signed Cloudinary URL.
    """
    try:
        frame = get_object_or_404(Frame.objects.only('id', 'title', 'audio_file', 'is_available'), id=frame_id, is_available=True)
        
        # Get or create statistics
        stats, created = Statistic.objects.get_or_create(frame=frame)
        stats.increment_scan()
        
        if not frame.audio_file:
            return Response({
                'error': 'No audio file found for this frame'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Generate signed URL for audio file
        signed_url = cloudinary.utils.cloudinary_url(
            frame.audio_file.name,
            resource_type="video",  # Cloudinary treats audio as video
            sign_url=True,
            expires_at=3600  # 1 hour expiry
        )[0]
        
        response_data = {
            'frame_id': frame.id,
            'frame_title': frame.title,
            'audio_url': frame.audio_file.url,
            'signed_audio_url': signed_url,
            'message': 'Audio file found successfully'
        }
        
        serializer = ScanResponseSerializer(response_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Error processing scan: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def track_play(request, frame_id):
    """
    Track audio play event.
    """
    try:
        frame = get_object_or_404(Frame.objects.only('id'), id=frame_id)
        stats, created = Statistic.objects.get_or_create(frame=frame)
        stats.increment_play()
        
        return Response({
            'message': 'Play tracked successfully',
            'plays_count': stats.plays_count
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Error tracking play: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminStatsView(APIView):
    """Admin dashboard statistics."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get admin statistics."""
        if not request.user.is_staff:
            return Response({
                'error': 'Admin access required'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Use cache for stats
        from django.core.cache import cache
        cache_key = 'admin_dashboard_stats'
        cached_stats = cache.get(cache_key)
        
        if cached_stats:
            return Response(cached_stats, status=status.HTTP_200_OK)
            
        # Calculate statistics
        total_orders = Order.objects.count()
        total_frames = Frame.objects.count()
        total_scans = Statistic.objects.aggregate(total=Sum('scans_count'))['total'] or 0
        total_plays = Statistic.objects.aggregate(total=Sum('plays_count'))['total'] or 0
        pending_orders = Order.objects.filter(status='pending').count()
        delivered_orders = Order.objects.filter(status='delivered').count()
        
        # Recent orders
        recent_orders = Order.objects.select_related('user', 'frame').order_by('-created_at')[:10]
        
        # Top frames by scans
        top_frames = Statistic.objects.select_related('frame').order_by('-scans_count')[:10]
        
        stats_data = {
            'total_orders': total_orders,
            'total_frames': total_frames,
            'total_scans': total_scans,
            'total_plays': total_plays,
            'pending_orders': pending_orders,
            'delivered_orders': delivered_orders,
            'recent_orders': recent_orders,
            'top_frames': top_frames,
        }
        
        serializer = AdminStatsSerializer(stats_data)
        serialized_data = serializer.data
        
        # Cache for 5 minutes
        cache.set(cache_key, serialized_data, 300)
        
        return Response(serialized_data, status=status.HTTP_200_OK)


class AudioUploadView(generics.CreateAPIView):
    """Upload audio file for a frame."""
    
    serializer_class = AudioUploadSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        frame_id = self.kwargs.get('frame_id')
        frame = get_object_or_404(Frame, id=frame_id, owner=self.request.user)
        
        # Update frame's audio file
        frame.audio_file = serializer.validated_data['audio_file']
        frame.save()
        
        # Create audio upload record
        serializer.save(frame=frame)


class UserFramesView(generics.ListAPIView):
    """Get frames owned by the current user."""
    
    serializer_class = FrameSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Frame.objects.filter(owner=self.request.user)


class UserOrdersView(generics.ListAPIView):
    """Get orders for the current user."""
    
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def compare_waveform_image(request):
    """
    Compare uploaded waveform image with stored waveform images.
    Returns the matching frame's audio URL if found.
    """
    try:
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image file provided'}, status=400)
        
        uploaded_image = request.FILES['image']
        
        # Get all frames with waveform images
        # Optimize: Only fetch necessary fields
        frames = Frame.objects.exclude(waveform_image='').only('id', 'waveform_image', 'audio_file', 'title', 'artist')
        
        best_match = None
        best_similarity = 0.0
        similarity_threshold = 0.7  # 70% similarity threshold
        
        # Convert uploaded image to OpenCV format
        uploaded_img_data = uploaded_image.read()
        uploaded_img_array = np.frombuffer(uploaded_img_data, np.uint8)
        uploaded_cv_img = cv2.imdecode(uploaded_img_array, cv2.IMREAD_COLOR)
        
        if uploaded_cv_img is None:
            return JsonResponse({'error': 'Invalid image format'}, status=400)
        
        # Use basic cache for stored images to avoid repeated downloads
        from django.core.cache import cache
        
        for frame in frames:
            try:
                # Cache stored image data
                img_cache_key = f'waveform_img_{frame.id}'
                stored_img_data = cache.get(img_cache_key)
                
                if not stored_img_data:
                    # Download the stored waveform image
                    stored_img_url = frame.waveform_image.url
                    response = requests.get(stored_img_url, timeout=5)
                    if response.status_code == 200:
                        stored_img_data = response.content
                        cache.set(img_cache_key, stored_img_data, 3600) # Cache for 1 hour
                
                if stored_img_data:
                    # Convert stored image to OpenCV format
                    stored_img_array = np.frombuffer(stored_img_data, np.uint8)
                    stored_cv_img = cv2.imdecode(stored_img_array, cv2.IMREAD_COLOR)
                    
                    if stored_cv_img is not None:
                        # Compare images
                        similarity = compare_images(uploaded_cv_img, stored_cv_img)
                        
                        if similarity > best_similarity:
                            best_similarity = similarity
                            best_match = frame
                            
            except Exception as e:
                print(f"Error processing frame {frame.id}: {str(e)}")
                continue
        
        # Check if we found a good match
        if best_match and best_similarity >= similarity_threshold:
            return JsonResponse({
                'success': True,
                'frame_id': best_match.id,
                'audio_url': best_match.audio_file.url if best_match.audio_file else None,
                'title': best_match.title,
                'artist': getattr(best_match, 'artist', ''),
                'similarity': best_similarity
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'No matching waveform found',
                'best_similarity': best_similarity
            }, status=404)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def compare_images(img1, img2):
    """
    Compare two images using structural similarity.
    Returns similarity score between 0 and 1.
    """
    try:
        from skimage.metrics import structural_similarity as ssim
        
        # Resize images to same size for comparison
        height, width = 200, 800  # Standard waveform dimensions
        img1_resized = cv2.resize(img1, (width, height))
        img2_resized = cv2.resize(img2, (width, height))
        
        # Convert to grayscale
        gray1 = cv2.cvtColor(img1_resized, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2_resized, cv2.COLOR_BGR2GRAY)
        
        # Calculate structural similarity
        similarity_score = ssim(gray1, gray2)
        
        return similarity_score
        
    except Exception as e:
        print(f"Error comparing images: {str(e)}")
        return 0.0
