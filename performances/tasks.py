from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import os
import sys
import subprocess
from django.conf import settings

logger = logging.getLogger(__name__)


def run_kopis_api():
    """주기적으로 kopis_api.py 파일을 실행하는 함수"""
    venv_python = sys.executable
    script_path = os.path.join(os.path.dirname(__file__), '..', 'kopis_api.py')

    try:
        result = subprocess.run(
            [venv_python, script_path], capture_output=True, text=True, encoding='utf-8')

        if result.returncode == 0:
            logger.info(f"Kopis API Success: {result.stdout}")
            run_loaddata()
        else:
            logger.error(f"Kopis API Error: {result.stderr}")

    except Exception as e:
        logger.error(f"Error running kopis_api.py: {e}")


def run_loaddata():
    """performance_370.json 데이터를 로드하는 함수"""
    venv_python = sys.executable
    manage_py_path = os.path.join(os.path.dirname(__file__), '..', 'manage.py')
    fixture_path = os.path.join(os.path.dirname(
        __file__), 'fixtures', 'performance_370.json')

    try:
        result = subprocess.run(
            [venv_python, manage_py_path, 'loaddata', fixture_path],
            capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            logger.info(f"Loaddata Success: {result.stdout}")
        else:
            logger.error(f"Loaddata Error: {result.stderr}")
    except Exception as e:
        logger.error(f"Error running loaddata: {e}")


def start_scheduler():
    """BackgroundScheduler를 시작하고 작업을 등록하는 함수"""
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")  # Django DB에 저장

    # 매일 자정에 kopis_api.py 파일 실행
    scheduler.add_job(
        run_kopis_api,
        trigger=CronTrigger(hour=00, minute=00),
        id='run_kopis_api_job',
        max_instances=1,
        replace_existing=True,
    )

    # 스케줄러 시작
    scheduler.start()
    logger.info("Scheduler started and job 'run_kopis_api' added.")
