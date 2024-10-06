import requests
import json
import os
import django
import xmltodict
from culturepedia import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'culturepedia.settings')
django.setup()

from performances.models import Performlist

api_key = config.API_KEY
performance_ids = Performlist.objects.values_list('kopis_id', flat=True)

performance_detail_res = []

for performance_code in performance_ids:
    url = f'http://www.kopis.or.kr/openApi/restful/pblprfr/{performance_code}?service={api_key}'
    response = requests.get(url)
    data = xmltodict.parse(response.content)

    for item in data['dbs']['db']:
        try:
            dict = {
                    "model" : "performances.performance",
                    "pk" : item['mt20id'],
                    'fields':
                    {
                        "title": item['prfnm'],
                        "state": item['prfstate'],
                        "start_date": item['prfpdfrom'],
                        "end_date": item['prfpdto'],
                        "facility_kopis_id": item['mt10id'],
                        "facility_name": item['fcltynm'],
                        "type": item['genrenm'],
                        "area": item['prfnm'],
                        "synopsis": item['sty'],
                        "cast": item['prfcast'],
                        "crew": item['prfcrew'],
                        "runtime": item['prfruntime'],
                        "age": item['prfage'],
                        "production": item['entrpsnmP'],
                        "agency": item['entrpsnmA'],
                        "pricing": item['pcseguidance'],                      
                        "visit": item['visit'],
                        "daehakro": item['daehakro'],
                        "festival": item['festival'],
                        "musicallicense": item['musicallicense'],
                        "musicalcreate": item['musicalcreate'],
                        "dtguidance": item['dtguidance'],
                        "poster": item['poster'],
                        "styurl": item['styurls'],
                    }
                    }
            performance_detail_res.append(dict)
        except:
            pass


with open('performances_detail.json', "w", encoding='utf-8') as f:

    json.dump(performance_detail_res, f, ensure_ascii=False, indent=4)