import requests
import xmltodict
import json
import os
import django
from culturepedia import settings
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'culturepedia.settings')  #Django 환경 설정 로드, 프로젝트 이름 지정
django.setup()

from performances.models import Performlist

api_key = settings.API_KEY

performance_res = []
existing_ids = set()  #중복확인 set

page_num = 1

while page_num < 2:

    start_date = datetime.now().strftime('%Y%m%d')
    end_date = (datetime.now() + timedelta(days=60)).strftime('%Y%m%d')


    url = f'http://www.kopis.or.kr/openApi/restful/pblprfr?service={api_key}&stdate={start_date}&eddate={end_date}&rows=5&cpage={page_num}'
    response = requests.get(url)
    data = xmltodict.parse(response.content)  # xml 파싱

    if data['dbs'] is None:
        break

    for item in data['dbs']['db']:
        try:
            mt20id = item['mt20id']
            title = item['prfnm']
            start_date = item['prfpdfrom']
            end_date = item['prfpdto']
            facility_name = item['fcltynm']
            type = item['genrenm']
            state = item['prfstate']

            # 공연ID 중복 체크
            try:
                performance = Performlist.objects.get(kopis_id=mt20id)

                # 업데이트 필요 필드 새로운 값 딕셔너리로 정리
                fields_to_update = {
                    "title": title,
                    "start_date": start_date,
                    "end_date": end_date,
                    "facility_name": facility_name,
                    "type": type,
                    "state": state,
                }

                updated = False  # 변경 여부 추적 플래그

                # 각 필드 비교 후 다른 경우 업데이트
                for field, new_value in fields_to_update.items():
                    if getattr(performance, field) != new_value:
                        setattr(performance, field, new_value)
                        updated = True

                # 변경 사항 저장
                if updated:
                    performance.save()
                    print(f'{mt20id}의 정보가 업데이트되었습니다.')

            # 없는 공연 생성
            except Performlist.DoesNotExist:
                dict_data = {
                    "model": "performances.Performlist",
                    "pk": item['mt20id'],
                    'fields': {
                        "title": item['prfnm'],
                        "start_date": item['prfpdfrom'],
                        "end_date": item['prfpdto'],
                        "facility_name": item['fcltynm'],
                        "type": item['genrenm'],
                        "state": item['prfstate'],
                    }
                }

                performance_res.append(dict_data)
                existing_ids.add(mt20id)

        except Exception as e:
            print(f"Error occurred: {e}")  # 오류 출력

    page_num += 1  # while True 시 페이지 증가

# 경로 설정
folder_path = 'performances/fixtures'
os.makedirs(folder_path, exist_ok=True)  # 폴더 없는 경우 생성

file_path = os.path.join(folder_path, 'performances_list.json')

# JSON 파일 저장
with open(file_path, "w", encoding='utf-8') as f:  # 파일 위치, write 쓰기, 문자 인코딩
    json.dump(performance_res, f, ensure_ascii=False, indent=4)  # 파싱 xml > json 변경 함수