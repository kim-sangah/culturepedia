from django.apps import AppConfig
from django.conf import settings


class PerformancesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'performances'

    def ready(self):
        from .tasks import start_scheduler
        start_scheduler()
