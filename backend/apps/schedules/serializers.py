from rest_framework import serializers
from .models import Schedule, Delay, MaintenanceSchedule
from apps.tracking.serializers import RouteSerializer, BusSerializer
from apps.users.serializers import DriverProfileSerializer

class ScheduleSerializer(serializers.ModelSerializer):
    route_details = RouteSerializer(source='route', read_only=True)
    bus_details = BusSerializer(source='bus', read_only=True)
    driver_details = DriverProfileSerializer(source='driver', read_only=True)

    class Meta:
        model = Schedule
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class DelaySerializer(serializers.ModelSerializer):
    schedule_details = ScheduleSerializer(source='schedule', read_only=True)

    class Meta:
        model = Delay
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'resolved_at')

class MaintenanceScheduleSerializer(serializers.ModelSerializer):
    bus_details = BusSerializer(source='bus', read_only=True)

    class Meta:
        model = MaintenanceSchedule
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'completed_at') 