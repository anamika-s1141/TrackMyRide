from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Bus, Route, Trip, LocationLog, EmergencyLog
from .serializers import (
    BusSerializer, RouteSerializer, TripSerializer,
    LocationLogSerializer, EmergencyLogSerializer, TripUpdateSerializer
)
from apps.users.models import DriverProfile

class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return Bus.objects.all()
        return Bus.objects.filter(is_active=True)

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return Route.objects.all()
        return Route.objects.filter(is_active=True)

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Trip.objects.all()
        elif user.role == 'DRIVER':
            return Trip.objects.filter(driver__user=user)
        return Trip.objects.filter(status='IN_PROGRESS')

    @action(detail=True, methods=['post'])
    def start_tracking(self, request, pk=None):
        trip = self.get_object()
        if trip.driver.user != request.user and request.user.role != 'ADMIN':
            return Response(
                {"error": "Not authorized to start tracking this trip"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        trip.is_tracking = True
        trip.status = Trip.Status.IN_PROGRESS
        trip.start_time = timezone.now()
        trip.save()
        
        return Response(TripSerializer(trip).data)

    @action(detail=True, methods=['post'])
    def stop_tracking(self, request, pk=None):
        trip = self.get_object()
        if trip.driver.user != request.user and request.user.role != 'ADMIN':
            return Response(
                {"error": "Not authorized to stop tracking this trip"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        trip.is_tracking = False
        trip.status = Trip.Status.COMPLETED
        trip.end_time = timezone.now()
        trip.save()
        
        return Response(TripSerializer(trip).data)

    @action(detail=True, methods=['post'])
    def update_location(self, request, pk=None):
        trip = self.get_object()
        if not trip.is_tracking:
            return Response(
                {"error": "Trip is not currently being tracked"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = TripUpdateSerializer(trip, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # Create location log
            location_data = {
                'trip': trip.id,
                'latitude': request.data.get('latitude'),
                'longitude': request.data.get('longitude'),
                'speed': request.data.get('speed')
            }
            location_serializer = LocationLogSerializer(data=location_data)
            if location_serializer.is_valid():
                location_serializer.save()
            
            return Response(TripSerializer(trip).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def report_emergency(self, request, pk=None):
        trip = self.get_object()
        if trip.driver.user != request.user and request.user.role != 'ADMIN':
            return Response(
                {"error": "Not authorized to report emergency for this trip"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        emergency_data = {
            'trip': trip.id,
            'emergency_type': request.data.get('emergency_type'),
            'description': request.data.get('description'),
            'location': request.data.get('location')
        }
        
        serializer = EmergencyLogSerializer(data=emergency_data)
        if serializer.is_valid():
            serializer.save()
            trip.status = Trip.Status.EMERGENCY
            trip.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 