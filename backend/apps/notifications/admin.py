from django.contrib import admin
from .models import Notification, NotificationPreference, BroadcastNotification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'notification_type', 'user', 'trip', 'route', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'user__username', 'user__email')
    readonly_fields = ('fcm_message_id',)
    date_hierarchy = 'created_at'

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_notifications', 'push_notifications')
    list_filter = (
        'delay_notifications', 'route_change_notifications', 'emergency_notifications',
        'ticket_notifications', 'payment_notifications', 'maintenance_notifications',
        'email_notifications', 'push_notifications'
    )
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('fcm_token',)

@admin.register(BroadcastNotification)
class BroadcastNotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'notification_type', 'route', 'sent_count', 'created_by', 'created_at')
    list_filter = ('notification_type', 'created_at')
    search_fields = ('title', 'message', 'created_by__username')
    readonly_fields = ('sent_count',)
    date_hierarchy = 'created_at' 