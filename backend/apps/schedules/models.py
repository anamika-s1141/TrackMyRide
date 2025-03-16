from django.db import models
from apps.tracking.models import Bus, Route
from apps.users.models import DriverProfile

class Schedule(models.Model):
    class Day(models.TextChoices):
        MONDAY = 'MON', 'Monday'
        TUESDAY = 'TUE', 'Tuesday'
        WEDNESDAY = 'WED', 'Wednesday'
        THURSDAY = 'THU', 'Thursday'
        FRIDAY = 'FRI', 'Friday'
        SATURDAY = 'SAT', 'Saturday'
        SUNDAY = 'SUN', 'Sunday'

    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='schedules')
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='schedules')
    driver = models.ForeignKey(DriverProfile, on_delete=models.SET_NULL, null=True, related_name='schedules')
    day_of_week = models.CharField(max_length=3, choices=Day.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.route.name} - {self.day_of_week} ({self.start_time}-{self.end_time})"

class Delay(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='delays')
    delay_minutes = models.PositiveIntegerField()
    reason = models.TextField()
    affected_date = models.DateField()
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.schedule} - {self.delay_minutes}min delay"

class MaintenanceSchedule(models.Model):
    class MaintenanceType(models.TextChoices):
        ROUTINE = 'ROUTINE', 'Routine Maintenance'
        REPAIR = 'REPAIR', 'Repair'
        INSPECTION = 'INSPECTION', 'Inspection'
        CLEANING = 'CLEANING', 'Cleaning'

    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='maintenance_schedules')
    maintenance_type = models.CharField(max_length=20, choices=MaintenanceType.choices)
    description = models.TextField()
    scheduled_date = models.DateField()
    estimated_duration_hours = models.PositiveIntegerField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bus} - {self.maintenance_type} on {self.scheduled_date}" 