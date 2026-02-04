"""
Serializers for the Audio Art Frame API.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Frame, Order, Statistic, AudioUpload


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class FrameSerializer(serializers.ModelSerializer):
    """Serializer for Frame model."""
    
    owner = UserSerializer(read_only=True)
    statistics = serializers.SerializerMethodField()
    
    class Meta:
        model = Frame
        fields = [
            'id', 'title', 'description', 'frame_type', 'image', 
            'qr_code', 'audio_file', 'owner', 'price', 'is_available',
            'created_at', 'updated_at', 'statistics'
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at', 'qr_code']
    
    def get_statistics(self, obj):
        """Get frame statistics."""
        try:
            stats = obj.statistics
            return {
                'scans_count': stats.scans_count,
                'plays_count': stats.plays_count,
                'last_scan': stats.last_scan,
                'last_play': stats.last_play,
            }
        except Statistic.DoesNotExist:
            return {
                'scans_count': 0,
                'plays_count': 0,
                'last_scan': None,
                'last_play': None,
            }


class FrameCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating frames."""
    
    class Meta:
        model = Frame
        fields = [
            'title', 'description', 'frame_type', 'image', 
            'audio_file', 'price', 'is_available'
        ]
    
    def create(self, validated_data):
        """Create frame and generate QR code."""
        frame = Frame.objects.create(**validated_data)
        frame.generate_qr_code()
        return frame


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model."""
    
    user = UserSerializer(read_only=True)
    frame = FrameSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'frame', 'customer_name', 'customer_phone',
            'customer_email', 'delivery_address', 'city', 'postal_code',
            'status', 'payment_method', 'total_amount', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating orders."""
    
    class Meta:
        model = Order
        fields = [
            'frame', 'customer_name', 'customer_phone', 'customer_email',
            'delivery_address', 'city', 'postal_code', 'wilaya', 'baladya',
            'audio_file', 'payment_method', 'notes'
        ]
    
    def create(self, validated_data):
        """Create order with user and calculate total amount."""
        user = self.context['request'].user
        frame = validated_data['frame']
        
        # Calculate total amount
        total_amount = frame.price
        
        # If audio file is provided, save it to the frame as well
        if 'audio_file' in validated_data and validated_data['audio_file']:
            frame.audio_file = validated_data['audio_file']
            frame.save()
        
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            **validated_data
        )
        return order


class StatisticSerializer(serializers.ModelSerializer):
    """Serializer for Statistic model."""
    
    frame_title = serializers.CharField(source='frame.title', read_only=True)
    
    class Meta:
        model = Statistic
        fields = [
            'id', 'frame', 'frame_title', 'scans_count', 'plays_count',
            'last_scan', 'last_play', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AudioUploadSerializer(serializers.ModelSerializer):
    """Serializer for AudioUpload model."""
    
    class Meta:
        model = AudioUpload
        fields = [
            'id', 'frame', 'audio_file', 'duration', 'file_size', 'uploaded_at'
        ]
        read_only_fields = ['id', 'uploaded_at']


class ScanResponseSerializer(serializers.Serializer):
    """Serializer for scan response."""
    
    frame_id = serializers.IntegerField()
    frame_title = serializers.CharField()
    audio_url = serializers.URLField()
    signed_audio_url = serializers.URLField()
    message = serializers.CharField()


class AdminStatsSerializer(serializers.Serializer):
    """Serializer for admin statistics."""
    
    total_orders = serializers.IntegerField()
    total_frames = serializers.IntegerField()
    total_scans = serializers.IntegerField()
    total_plays = serializers.IntegerField()
    pending_orders = serializers.IntegerField()
    delivered_orders = serializers.IntegerField()
    recent_orders = OrderSerializer(many=True)
    top_frames = StatisticSerializer(many=True)
