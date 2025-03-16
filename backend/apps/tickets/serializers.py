from rest_framework import serializers
from .models import Ticket, TicketValidation
from apps.users.serializers import StudentProfileSerializer, UserSerializer
from apps.tracking.serializers import TripSerializer

class TicketSerializer(serializers.ModelSerializer):
    student_details = StudentProfileSerializer(source='student', read_only=True)
    trip_details = TripSerializer(source='trip', read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ('payment_id', 'created_at', 'updated_at')

class TicketValidationSerializer(serializers.ModelSerializer):
    ticket_details = TicketSerializer(source='ticket', read_only=True)
    trip_details = TripSerializer(source='trip', read_only=True)
    validated_by_details = UserSerializer(source='validated_by', read_only=True)

    class Meta:
        model = TicketValidation
        fields = '__all__'
        read_only_fields = ('validated_at', 'location')

class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['ticket_type', 'student']

class TicketValidationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketValidation
        fields = ['ticket', 'trip', 'location'] 