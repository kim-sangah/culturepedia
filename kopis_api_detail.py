import requests
import json
import os
import django
import xmltodict
from culturepedia import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'culturepedia.settings')
django.setup()

from performances.models import Performlist

performancedetail_res = []

api_key = config.API_KEY
performance_ids = list(Performlist.objects.values_list('kopis_id', flat=True))

for performance_code in performance_ids:
    url = f'http://www.kopis.or.kr/openApi/restful/pblprfr/{performance_code}?service={api_key}'
    response = requests.get(url)
    data = xmltodict.parse(response.content)

    db_data = data['dbs']['db']

    if isinstance(db_data, dict):
            try:
                    performance_dict = {
                    "model": "performances.performance",
                    "pk": db_data['mt20id'],
                    'fields': 
                    {
                        "title": db_data['prfnm'],
                        "state": db_data['prfstate'],
                        "start_date": db_data.get('prfpdfrom', 'N/A'),
                        "end_date": db_data.get('prfpdto', 'N/A'),
                        "facility_kopis_id": db_data.get('mt10id', 'N/A'),
                        "facility_name": db_data.get('fcltynm', 'N/A'),
                        "type": db_data.get('genrenm', 'N/A'),
                        "area": db_data.get('area', 'N/A'),
                        "synopsis": db_data.get('sty', 'N/A'),
                        "cast": db_data.get('prfcast', 'N/A'),
                        "crew": db_data.get('prfcrew', 'N/A'),
                        "runtime": db_data.get('prfruntime', 'N/A'),
                        "age": db_data.get('prfage', 'N/A'),
                        "production": db_data.get('entrpsnmP', 'N/A'),
                        "agency": db_data.get('entrpsnmA', 'N/A'),
                        "pricing": db_data.get('pcseguidance', 'N/A'),
                        "visit": db_data['visit'],
                        "daehakro": db_data['daehakro'],
                        "festival": db_data['festival'],
                        "musicallicense": db_data['musicallicense'],
                        "musicalcreate": db_data['musicalcreate'],
                        "dtguidance": db_data.get('dtguidance', 'N/A'),
                        "poster": db_data.get('poster', 'N/A'),
                        "styurl": db_data.get('styurls', 'N/A'),
                    }
                    }
                    performancedetail_res.append(performance_dict)
            except:
                pass
    else:
        pass

with open('performances_detail.json', "w", encoding='utf-8') as f:

    json.dump(performancedetail_res, f, ensure_ascii=False, indent=4)