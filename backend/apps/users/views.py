from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from .models import DriverProfile, StudentProfile
from .serializers import UserSerializer, DriverProfileSerializer, StudentProfileSerializer
from .permissions import IsAdminUser

User = get_user_model()

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if user:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_user(request):
    logout(request)
    return Response({'detail': 'Successfully logged out.'})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'detail': 'User activated successfully'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'detail': 'User deactivated successfully'})

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class DriverProfileViewSet(viewsets.ModelViewSet):
    queryset = DriverProfile.objects.all()
    serializer_class = DriverProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return DriverProfile.objects.all()
        elif self.request.user.role == 'DRIVER':
            return DriverProfile.objects.filter(user=self.request.user)
        return DriverProfile.objects.none()

    @action(detail=True, methods=['post'])
    def toggle_duty(self, request, pk=None):
        profile = self.get_object()
        profile.is_on_duty = not profile.is_on_duty
        profile.save()
        return Response({
            'detail': f"Driver is {'on' if profile.is_on_duty else 'off'} duty"
        })

class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return StudentProfile.objects.all()
        elif self.request.user.role == 'STUDENT':
            return StudentProfile.objects.filter(user=self.request.user)
        return StudentProfile.objects.none()

    @action(detail=True, methods=['post'])
    def toggle_subscription(self, request, pk=None):
        profile = self.get_object()
        profile.is_subscription_active = not profile.is_subscription_active
        profile.save()
        return Response({
            'detail': f"Subscription {'activated' if profile.is_subscription_active else 'deactivated'}"
        }) 