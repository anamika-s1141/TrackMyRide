from django.apps import AppConfig

class TicketsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tickets'
    verbose_name = 'Bus Tickets'

    def ready(self):
        import apps.tickets.signals  # Import signals 