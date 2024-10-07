from django_apscheduler import jobstores
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import os
import sys
import subprocess
from django.conf import settings

logger = logging.getLogger(__name__)


# JSON 파일을 생성하는 함수
def run_script(script_name):
    venv_python = sys.executable
    script_path = os.path.join(os.path.dirname(__file__), '..', script_name)

    try:
        result = subprocess.run(
            [venv_python, script_path], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"{script_name} Success: {result.stdout}")
            return True
        else:
            print(f"{script_name} Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error running {script_name}: {e}")
        return False


# JSON 데이터를 DB에 저장하는 함수
def run_loaddata(fixture_name):
    venv_python = sys.executable
    manage_py_path = os.path.join(os.path.dirname(__file__), '..', 'manage.py')
    fixture_path = os.path.join(os.path.dirname(
        __file__), 'fixtures', fixture_name)

    try:
        result = subprocess.run([venv_python, manage_py_path, 'loaddata', fixture_path],
                                capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"Loaddata {fixture_name} Success: {result.stdout}")
        else:
            print(f"Loaddata {fixture_name} Error: {result.stderr}")
    except Exception as e:
        print(f"Error running loaddata for {fixture_name}: {e}")


# 순차적으로 실행(공연전체 -> 공연장 -> 공연상세)
def process_scripts():
    # 1. kopis_api.py 실행
    if run_script('kopis_api.py'):
        run_loaddata('performances_list.json')  # kopis_api의 데이터를 로드
    else:
        return

    # 2. facility_api.py 실행
    if run_script('facility_api.py'):
        run_loaddata('facility.json')  # facility_api의 데이터를 로드
    else:
        return

    # 3. kopis_detail_api.py 실행
    if run_script('kopis_detail_api.py'):
        # kopis_detail_api의 데이터를 로드
        run_loaddata('performances_detail.json')
    else:
        return


def start_scheduler():
    """BackgroundScheduler를 시작하고 작업을 등록하는 함수"""
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(jobstores.DjangoJobStore(),
                           "default")  # Django DB에 저장

    # 매일 자정에 run_all_scripts 실행
    scheduler.add_job(
        process_scripts,
        trigger=CronTrigger(hour=15, minute=24),
        id='process_scripts',
        max_instances=1,
        replace_existing=True,
    )

    # 스케줄러 시작
    scheduler.start()
    print("Scheduler started and job 'process_scripts' added.")
