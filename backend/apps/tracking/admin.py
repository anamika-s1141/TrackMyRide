from django.contrib import admin
from .models import Bus, Route, Trip, LocationLog, EmergencyLog

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_number', 'capacity', 'current_driver', 'is_active', 'last_maintenance')
    list_filter = ('is_active', 'last_maintenance')
    search_fields = ('bus_number', 'current_driver__user__username')

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'estimated_duration', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('route', 'bus', 'driver', 'status', 'start_time', 'end_time', 'passenger_count')
    list_filter = ('status', 'start_time', 'is_tracking')
    search_fields = ('route__name', 'bus__bus_number', 'driver__user__username')
    date_hierarchy = 'start_time'

@admin.register(LocationLog)
class LocationLogAdmin(admin.ModelAdmin):
    list_display = ('trip', 'latitude', 'longitude', 'speed', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('trip__route__name',)
    date_hierarchy = 'timestamp'

@admin.register(EmergencyLog)
class EmergencyLogAdmin(admin.ModelAdmin):
    list_display = ('trip', 'emergency_type', 'is_resolved', 'created_at')
    list_filter = ('emergency_type', 'is_resolved', 'created_at')
    search_fields = ('trip__route__name', 'description')
    date_hierarchy = 'created_at' 