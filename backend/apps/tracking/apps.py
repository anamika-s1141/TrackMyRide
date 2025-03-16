from django.apps import AppConfig

class TrackingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tracking'
    verbose_name = 'Bus Tracking'

    def ready(self):
        import apps.tracking.signals  # Import signals 