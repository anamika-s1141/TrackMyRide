from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScheduleViewSet, DelayViewSet, MaintenanceScheduleViewSet

router = DefaultRouter()
router.register(r'schedules', ScheduleViewSet)
router.register(r'delays', DelayViewSet)
router.register(r'maintenance', MaintenanceScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 