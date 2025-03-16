from django.db import models
from apps.users.models import User, DriverProfile

class Bus(models.Model):
    bus_number = models.CharField(max_length=50, unique=True)
    capacity = models.PositiveIntegerField()
    current_driver = models.ForeignKey(DriverProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_bus')
    is_active = models.BooleanField(default=True)
    last_maintenance = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bus {self.bus_number}"

class Route(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    stops = models.JSONField()  # List of stops with coordinates
    estimated_duration = models.DurationField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Trip(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = 'NOT_STARTED', 'Not Started'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        EMERGENCY = 'EMERGENCY', 'Emergency'

    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    current_location = models.JSONField(null=True, blank=True)
    current_stop_index = models.IntegerField(default=0)
    passenger_count = models.PositiveIntegerField(default=0)
    is_tracking = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.route.name} - {self.bus.bus_number} - {self.status}"

class LocationLog(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='location_logs')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    speed = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trip} - {self.timestamp}"

class EmergencyLog(models.Model):
    class EmergencyType(models.TextChoices):
        MECHANICAL = 'MECHANICAL', 'Mechanical Issue'
        MEDICAL = 'MEDICAL', 'Medical Emergency'
        ACCIDENT = 'ACCIDENT', 'Accident'
        OTHER = 'OTHER', 'Other'

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    emergency_type = models.CharField(max_length=20, choices=EmergencyType.choices)
    description = models.TextField()
    location = models.JSONField()
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trip} - {self.emergency_type} - {self.created_at}" 