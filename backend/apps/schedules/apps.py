from django.apps import AppConfig

class SchedulesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.schedules'
    verbose_name = 'Bus Schedules'

    def ready(self):
        import apps.schedules.signals  # Import signals 