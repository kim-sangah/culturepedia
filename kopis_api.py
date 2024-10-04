import requests
import json
import os
import django
import xmltodict
from culturepedia import config

# Django 환경 설정 로드
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'culturepedia.settings')  # 프로젝트 이름을 지정
django.setup()

from performances.models import Performance

api_key = config.API_KEY

performance_res = []
existing_ids = set()  # 중복 확인을 위한 set

for pageNum in range(1, 37):
    url = f'http://www.kopis.or.kr/openApi/restful/pblprfr?service={api_key}&stdate=20240901&eddate=20241030&rows=100&cpage={pageNum}'
    response = requests.get(url)
    data = xmltodict.parse(response.content)

    for item in data['dbs']['db']:
        try:
            mt20id = item['mt20id']
            facility_name = item['fcltynm']
            start_date = item['prfpdfrom']
            end_date = item['prfpdto']
            performance_type = item['genrenm']
            state = item['prfstate']

            # 공연ID 중복 체크
            try:
                performance = Performance.objects.get(kopis_id=mt20id)

                # 업데이트가 필요한 필드들과 새로운 값을 딕셔너리로 정리
                fields_to_update = {
                    "facility_name": facility_name,
                    "start_date": start_date,
                    "end_date": end_date,
                    "type": performance_type,
                    "state": state,
                }

                updated = False  # 변경 여부를 추적하는 플래그

                # 각 필드를 비교하고, 다를 경우 업데이트
                for field, new_value in fields_to_update.items():
                    if getattr(performance, field) != new_value:
                        setattr(performance, field, new_value)
                        updated = True

                # 변경 사항이 있으면 저장
                if updated:
                    performance.save()
                    print(f'{mt20id}의 정보가 업데이트되었습니다.')

            # 공연이 없으면 생성
            except Performance.DoesNotExist:
                dict_data = {
                    "model": "performances.performance",
                    "pk": item['mt20id'],
                    'fields': {
                        "title": item['prfnm'],
                        "start_date": item['prfpdfrom'],
                        "end_date": item['prfpdto'],
                        "facility_name": item['fcltynm'],
                        "type": item['genrenm'],
                        "state": state,
                    }
                }

                performance_res.append(dict_data)
                existing_ids.add(mt20id)

        except Exception as e:
            print(f"Error occurred: {e}")  # 오류 출력

# 경로 설정
folder_path = 'performances/fixtures'
os.makedirs(folder_path, exist_ok=True)  # 폴더가 없으면 생성

file_path = os.path.join(folder_path, 'performance_370.json')

# JSON 파일 저장
with open(file_path, "w", encoding='utf-8') as f:
    json.dump(performance_res, f, ensure_ascii=False, indent=4)
