from django.contrib import admin
from .models import Schedule, Delay, MaintenanceSchedule

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('route', 'bus', 'driver', 'day_of_week', 'start_time', 'end_time', 'is_active')
    list_filter = ('day_of_week', 'is_active', 'route', 'bus')
    search_fields = ('route__name', 'bus__bus_number', 'driver__user__username')
    date_hierarchy = 'created_at'

@admin.register(Delay)
class DelayAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'delay_minutes', 'affected_date', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'affected_date', 'created_at')
    search_fields = ('schedule__route__name', 'reason')
    date_hierarchy = 'affected_date'

@admin.register(MaintenanceSchedule)
class MaintenanceScheduleAdmin(admin.ModelAdmin):
    list_display = ('bus', 'maintenance_type', 'scheduled_date', 'estimated_duration_hours', 'is_completed')
    list_filter = ('maintenance_type', 'is_completed', 'scheduled_date')
    search_fields = ('bus__bus_number', 'description', 'notes')
    date_hierarchy = 'scheduled_date' 