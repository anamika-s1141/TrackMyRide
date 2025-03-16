from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        DRIVER = 'DRIVER', 'Driver'
        STUDENT = 'STUDENT', 'Student'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    phone_number = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.role}"

class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    license_number = models.CharField(max_length=50)
    years_of_experience = models.PositiveIntegerField(default=0)
    is_on_duty = models.BooleanField(default=False)
    current_location = models.JSONField(null=True, blank=True)
    last_active = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Driver: {self.user.username}"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100)
    semester = models.PositiveIntegerField()
    is_subscription_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Student: {self.user.username}" 