from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Schedule, Delay, MaintenanceSchedule
from .serializers import ScheduleSerializer, DelaySerializer, MaintenanceScheduleSerializer
from apps.users.permissions import IsAdminUser, IsDriverUser

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def current_week(self):
        today = timezone.now().date()
        start_of_week = today - timezone.timedelta(days=today.weekday())
        end_of_week = start_of_week + timezone.timedelta(days=6)
        schedules = self.queryset.filter(
            created_at__date__range=[start_of_week, end_of_week]
        )
        serializer = self.get_serializer(schedules, many=True)
        return Response(serializer.data)

class DelayViewSet(viewsets.ModelViewSet):
    queryset = Delay.objects.all()
    serializer_class = DelaySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated(), IsDriverUser()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        delay = self.get_object()
        if delay.is_resolved:
            return Response(
                {'detail': 'Delay is already resolved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        delay.is_resolved = True
        delay.resolved_at = timezone.now()
        delay.save()
        return Response({'detail': 'Delay marked as resolved'})

class MaintenanceScheduleViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceSchedule.objects.all()
    serializer_class = MaintenanceScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        maintenance = self.get_object()
        if maintenance.is_completed:
            return Response(
                {'detail': 'Maintenance is already completed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        maintenance.is_completed = True
        maintenance.completed_at = timezone.now()
        maintenance.save()
        return Response({'detail': 'Maintenance marked as completed'})