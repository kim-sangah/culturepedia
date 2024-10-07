import requests
import json
import os
import django
import xmltodict
from culturepedia import config

# Django 환경 설정 로드
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'culturepedia.settings')  # 프로젝트 이름을 지정
django.setup()

api_key = config.API_KEY

performance_res = []

for pageNum in range(1, 37):
    url = f'http://www.kopis.or.kr/openApi/restful/pblprfr?service={api_key}&stdate=20240901&eddate=20241030&rows=100&cpage={pageNum}'
    response = requests.get(url)
    data = xmltodict.parse(response.content)

    for item in data['dbs']['db']:
        try:
            dict = {
                    "model" : "performances.Performlist",
                    "pk" : item['mt20id'],
                    'fields':
                    {
                        "title": item['prfnm'],
                        "start_date": item['prfpdfrom'],
                        "end_date": item['prfpdto'],
                        "facility_name": item['fcltynm'],
                        "type": item['genrenm'],
                        "state": item['prfstate']
                    }
                    }
            performance_res.append(dict)
        except:
            pass    

folder_path = 'performances/fixtures'
os.makedirs(folder_path, exist_ok=True)

file_path = os.path.join(folder_path, 'performance_370.json')

with open('performances_list.json', "w", encoding='utf-8') as f:

    json.dump(performance_res, f, ensure_ascii=False, indent=4)