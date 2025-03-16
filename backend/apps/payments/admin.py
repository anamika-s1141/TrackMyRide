from django.contrib import admin
from .models import Payment, RefundRequest

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'amount', 'currency', 'status', 'paid_at', 'created_at')
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('ticket__id', 'stripe_payment_intent_id')
    readonly_fields = ('stripe_payment_intent_id', 'stripe_payment_method_id', 'receipt_url')
    date_hierarchy = 'created_at'

@admin.register(RefundRequest)
class RefundRequestAdmin(admin.ModelAdmin):
    list_display = ('payment', 'status', 'requested_by', 'approved_by', 'refunded_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('payment__ticket__id', 'stripe_refund_id', 'requested_by__email')
    readonly_fields = ('stripe_refund_id',)
    date_hierarchy = 'created_at' 