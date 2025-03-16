from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, DriverProfileViewSet, StudentProfileViewSet,
    register_user, logout_user
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'drivers', DriverProfileViewSet)
router.register(r'students', StudentProfileViewSet)

urlpatterns = [
    path('register/', register_user, name='register'),
    path('logout/', logout_user, name='logout'),
    path('', include(router.urls)),
] 