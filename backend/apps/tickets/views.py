from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Ticket, TicketValidation
from .serializers import (
    TicketSerializer, TicketValidationSerializer,
    TicketCreateSerializer, TicketValidationCreateSerializer
)
from apps.users.permissions import IsAdminUser, IsDriverUser

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return Ticket.objects.all()
        elif self.request.user.role == 'STUDENT':
            return Ticket.objects.filter(student__user=self.request.user)
        return Ticket.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return TicketCreateSerializer
        return TicketSerializer

    @action(detail=True, methods=['post'])
    def validate(self, request, pk=None):
        ticket = self.get_object()
        trip_id = request.data.get('trip_id')
        location = request.data.get('location')

        if not trip_id or not location:
            return Response(
                {'detail': 'Trip ID and location are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if ticket.status != Ticket.Status.APPROVED:
            return Response(
                {'detail': 'Ticket is not approved'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if ticket.valid_until and ticket.valid_until < timezone.now():
            return Response(
                {'detail': 'Ticket has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )

        validation = TicketValidation.objects.create(
            ticket=ticket,
            trip_id=trip_id,
            location=location,
            validated_by=request.user
        )

        ticket.status = Ticket.Status.USED
        ticket.save()

        return Response(TicketValidationSerializer(validation).data)

class TicketValidationViewSet(viewsets.ModelViewSet):
    queryset = TicketValidation.objects.all()
    serializer_class = TicketValidationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated(), IsDriverUser()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return TicketValidation.objects.all()
        elif self.request.user.role == 'DRIVER':
            return TicketValidation.objects.filter(validated_by=self.request.user)
        elif self.request.user.role == 'STUDENT':
            return TicketValidation.objects.filter(ticket__student__user=self.request.user)
        return TicketValidation.objects.none() 