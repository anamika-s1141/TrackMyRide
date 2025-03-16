from rest_framework import serializers
from .models import Bus, Route, Trip, LocationLog, EmergencyLog
from apps.users.serializers import DriverProfileSerializer

class BusSerializer(serializers.ModelSerializer):
    current_driver = DriverProfileSerializer(read_only=True)
    
    class Meta:
        model = Bus
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    bus = BusSerializer(read_only=True)
    route = RouteSerializer(read_only=True)
    driver = DriverProfileSerializer(read_only=True)
    
    class Meta:
        model = Trip
        fields = '__all__'

class LocationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationLog
        fields = '__all__'

class EmergencyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyLog
        fields = '__all__'

class TripUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['status', 'current_location', 'current_stop_index', 'passenger_count', 'is_tracking'] 