import requests
import json
import os
import django
import xmltodict
from culturepedia import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'culturepedia.settings')
django.setup()

from performances.models import Performance

api_key = config.API_KEY
facility_ids = Performance.objects.values_list('facility_kopis_id', flat=True)

facility_res = []

for facility_code in facility_ids:
    url = f'http://www.kopis.or.kr/openApi/restful/prfplc/{facility_code}?service={api_key}'
    response = requests.get(url)
    data = xmltodict.parse(response.content)

    for item in data['dbs']['db']:
        try:
            dict = {
                    "model" : "performances.facility",
                    "pk" : item['mt10id'],
                    'fields':
                    {
                        "name": item['fcltynm'],
                        "seatscale": item['seatscale'],
                        "relateurl": item['relateurl'],
                        "address": item['adres'],
                        "telno": item['telno'],
                    }
                    }
            facility_res.append(dict)
        except:
            pass


with open('facility.json', "w", encoding='utf-8') as f:

    json.dump(facility_res, f, ensure_ascii=False, indent=4)