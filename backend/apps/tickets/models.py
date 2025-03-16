from django.db import models
from apps.users.models import User, StudentProfile
from apps.tracking.models import Trip

class Ticket(models.Model):
    class TicketType(models.TextChoices):
        SINGLE = 'SINGLE', 'Single Journey'
        DAILY = 'DAILY', 'Daily Pass'
        WEEKLY = 'WEEKLY', 'Weekly Pass'
        MONTHLY = 'MONTHLY', 'Monthly Pass'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        USED = 'USED', 'Used'
        EXPIRED = 'EXPIRED', 'Expired'

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.CharField(max_length=10, choices=TicketType.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.ticket_type} - {self.status}"

class TicketValidation(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='validations')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    validated_at = models.DateTimeField(auto_now_add=True)
    location = models.JSONField()
    validated_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ticket} - {self.validated_at}" 