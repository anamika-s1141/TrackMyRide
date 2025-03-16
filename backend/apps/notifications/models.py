from django.db import models
from apps.users.models import User
from apps.tracking.models import Trip, Route

class NotificationType(models.TextChoices):
    DELAY = 'DELAY', 'Delay'
    ROUTE_CHANGE = 'ROUTE_CHANGE', 'Route Change'
    EMERGENCY = 'EMERGENCY', 'Emergency'
    TICKET = 'TICKET', 'Ticket'
    PAYMENT = 'PAYMENT', 'Payment'
    MAINTENANCE = 'MAINTENANCE', 'Maintenance'
    GENERAL = 'GENERAL', 'General'

class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    is_read = models.BooleanField(default=False)
    data = models.JSONField(null=True, blank=True)  # Additional data for the notification
    fcm_message_id = models.CharField(max_length=100, null=True, blank=True)  # Firebase Cloud Messaging ID
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.notification_type} - {self.user.username}"

class NotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    delay_notifications = models.BooleanField(default=True)
    route_change_notifications = models.BooleanField(default=True)
    emergency_notifications = models.BooleanField(default=True)
    ticket_notifications = models.BooleanField(default=True)
    payment_notifications = models.BooleanField(default=True)
    maintenance_notifications = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    fcm_token = models.CharField(max_length=255, null=True, blank=True)  # Firebase Cloud Messaging token

    def __str__(self):
        return f"Preferences for {self.user.username}"

class BroadcastNotification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True)
    roles = models.JSONField(help_text='List of user roles to receive this notification')
    data = models.JSONField(null=True, blank=True)
    sent_count = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Broadcast: {self.title}" 