import firebase_admin
from firebase_admin import messaging
from django.conf import settings
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Notification, NotificationPreference, BroadcastNotification
from .serializers import (
    NotificationSerializer, NotificationPreferenceSerializer,
    BroadcastNotificationSerializer
)
from apps.users.permissions import IsAdminUser
from config.firebase import send_notification, send_multicast_notification

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'detail': 'Notification marked as read'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        self.get_queryset().update(is_read=True)
        return Response({'detail': 'All notifications marked as read'})

class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NotificationPreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def update_fcm_token(self, request, pk=None):
        preference = self.get_object()
        token = request.data.get('fcm_token')
        if not token:
            return Response(
                {'detail': 'FCM token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        preference.fcm_token = token
        preference.save()
        return Response({'detail': 'FCM token updated'})

class BroadcastNotificationViewSet(viewsets.ModelViewSet):
    queryset = BroadcastNotification.objects.all()
    serializer_class = BroadcastNotificationSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        broadcast = self.get_object()
        preferences = NotificationPreference.objects.filter(
            user__role__in=broadcast.roles,
            push_notifications=True
        ).exclude(fcm_token__isnull=True)

        tokens = [pref.fcm_token for pref in preferences]
        if tokens:
            result = send_multicast_notification(
                tokens=tokens,
                title=broadcast.title,
                body=broadcast.message,
                data=broadcast.data
            )
            if result:
                broadcast.sent_count = len(tokens)
                broadcast.save()
                return Response({'detail': f'Notification sent to {len(tokens)} devices'})
        return Response(
            {'detail': 'No valid recipients found'},
            status=status.HTTP_400_BAD_REQUEST
        )

def send_push_notification(user, title, message, data=None):
    try:
        preference = NotificationPreference.objects.get(user=user)
        
        if not preference.push_notifications or not preference.fcm_token:
            return
        
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=message
            ),
            data=data if data else {},
            token=preference.fcm_token
        )
        
        response = messaging.send(message)
        return response
        
    except Exception as e:
        print(f"Error sending push notification: {e}")
        return None 