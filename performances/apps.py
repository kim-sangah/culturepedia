from django.apps import AppConfig
from django.conf import settings
import os
from .tasks import start_scheduler


class PerformancesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'performances'

    def ready(self):
        # RUN_MAIN 이 'true' 인 경우에 스케쥴러 실행
        if os.environ.get('RUN_MAIN', None) is not None:
            # print(' RUN_MAIN :', os.environ.get('RUN_MAIN', None))
            start_scheduler()
