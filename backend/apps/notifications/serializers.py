from rest_framework import serializers
from .models import Notification, NotificationPreference, BroadcastNotification
from apps.users.serializers import UserSerializer
from apps.tracking.serializers import TripSerializer, RouteSerializer

class NotificationSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    trip_details = TripSerializer(source='trip', read_only=True)
    route_details = RouteSerializer(source='route', read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('created_at', 'fcm_message_id')

class NotificationPreferenceSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = NotificationPreference
        fields = '__all__'
        read_only_fields = ('fcm_token',)

class BroadcastNotificationSerializer(serializers.ModelSerializer):
    route_details = RouteSerializer(source='route', read_only=True)
    created_by_details = UserSerializer(source='created_by', read_only=True)

    class Meta:
        model = BroadcastNotification
        fields = '__all__'
        read_only_fields = ('sent_count', 'created_at') 