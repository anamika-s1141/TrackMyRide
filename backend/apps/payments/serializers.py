from rest_framework import serializers
from .models import Payment, RefundRequest
from apps.tickets.serializers import TicketSerializer
from apps.users.serializers import UserSerializer

class PaymentSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'

class RefundRequestSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    requested_by = UserSerializer(read_only=True)
    approved_by = UserSerializer(read_only=True)
    
    class Meta:
        model = RefundRequest
        fields = '__all__'

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['ticket', 'amount', 'currency']

class RefundRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefundRequest
        fields = ['payment', 'reason'] 