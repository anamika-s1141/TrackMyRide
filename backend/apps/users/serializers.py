from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import DriverProfile, StudentProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'phone_number', 'is_active', 'date_joined')
        read_only_fields = ('date_joined',)

class DriverProfileSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = DriverProfile
        fields = '__all__'
        read_only_fields = ('current_location', 'last_active')

class StudentProfileSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = StudentProfile
        fields = '__all__'
        read_only_fields = ('is_subscription_active',)