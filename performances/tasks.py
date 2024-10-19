from django_apscheduler import jobstores
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import os
import sys
import subprocess
import requests
from django.conf import settings


# JSON 파일을 생성 함수
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


# JSON 데이터 > DB 저장 함수
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


# hashtag 생성 실행
def endpoint_script(url):
    try:
        response = requests.post(
            f'http://3.36.66.92/api/performances/{url}/')
        if response.status_code == 200:
            print("Successfully called the API endpoint.")
        else:
            print(f"Error calling API: {response.status_code}")
    except Exception as e:
        print(f"Exception occurred: {e}")


# 실행 순서 (공연목록 > 공연장 > 공연상세)


def process_scripts():
    # 1. kopis_api.py 실행
    if run_script('kopis_api.py'):
        run_loaddata('performances_list.json')  # kopis_api 데이터 로드
    else:
        return

    # 2. kopis_api_detail.py 실행
    if run_script('kopis_api_detail.py'):
        # 3. facility_api.py 실행
        if run_script('facility_api.py'):
            run_loaddata('facility.json')  # facility_api 데이터 로드
            # kopis_api_detail 데이터 로드
            run_loaddata('performances_detail.json')
            # 4. hashtag endpoint 실행
            endpoint_script('hashtag')
    else:
        return


# BackgroundScheduler 실행 및 작업 등록 함수
def start_scheduler():
    if not hasattr(start_scheduler, 'scheduler_running'):
        scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(jobstores.DjangoJobStore(), "default")  # Django DB에 저장

        # 매일 자정 procees_scripts 실행
        scheduler.add_job(
            process_scripts,
            trigger=CronTrigger(hour=23, minute=38),
            id='process_scripts',
            max_instances=1,
            replace_existing=True,
        )

        # 스케줄러 실행
        scheduler.start()
        print("Scheduler started and job 'process_scripts' added.")
    else:
        print("Scheduler is already running.")
