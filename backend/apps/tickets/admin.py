from django.contrib import admin
from .models import Ticket, TicketValidation

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('student', 'ticket_type', 'status', 'valid_from', 'valid_until', 'price', 'created_at')
    list_filter = ('ticket_type', 'status', 'created_at')
    search_fields = ('student__user__username', 'student__student_id', 'payment_id')
    readonly_fields = ('payment_id',)
    date_hierarchy = 'created_at'

@admin.register(TicketValidation)
class TicketValidationAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'trip', 'validated_by', 'validated_at')
    list_filter = ('validated_at',)
    search_fields = ('ticket__student__user__username', 'validated_by__username')
    readonly_fields = ('location',)
    date_hierarchy = 'validated_at' 