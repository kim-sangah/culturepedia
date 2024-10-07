import requests
import json
import os
import django
import xmltodict
from culturepedia import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'culturepedia.settings')
django.setup()

from performances.models import Facility

with open('performances/fixtures/performances_detail.json', 'r', encoding='utf-8') as f:
    performances_detail = json.load(f)

api_key = config.API_KEY
facility_ids = [performance['fields']['facility_kopis_id'] for performance in performances_detail]

facility_res = []
existing_ids = set()

for facility_code in facility_ids:
    url = f'http://www.kopis.or.kr/openApi/restful/prfplc/{facility_code}?service={api_key}'
    response = requests.get(url)
    data = xmltodict.parse(response.content)

    db_data = data['dbs']['db']

    if isinstance(db_data, dict):
        try:
            mt10id = db_data['mt10id']
            name = db_data['fcltynm']
            seatscale = db_data['seatscale']
            relateurl = db_data['relateurl']
            address = db_data['adres']
            telno = db_data['telno']

            try:
                facility = Facility.objects.get(kopis_id=mt10id)

                fields_to_update = {
                    "name": name,
                    "seatscale": seatscale,
                    "relateurl": relateurl,
                    "address": address,
                    "telno": telno,
                }

                updated = False 

                for field, new_value in fields_to_update.items():
                    if getattr(facility, field) != new_value:
                        setattr(facility, field, new_value)
                        updated = True

                if updated:
                    facility.save()
                    print(f'{mt10id}의 정보가 업데이트되었습니다.')

            except Facility.DoesNotExist:
                facility_dict = {
                        "model" : "performances.facility",
                        "pk" : db_data['mt10id'],
                        'fields':
                        {
                            "name": db_data['fcltynm'],
                            "seatscale": db_data['seatscale'],
                            "relateurl": db_data['relateurl'],
                            "address": db_data['adres'],
                            "telno": db_data['telno'],
                        }
                        }
                facility_res.append(facility_dict)
                existing_ids.add(mt10id)

        except Exception as e:
            print(f"Error occurred: {e}")
    else:
        pass

folder_path = 'performances/fixtures'
os.makedirs(folder_path, exist_ok=True)

file_path = os.path.join(folder_path, 'facility.json')

with open(file_path, "w", encoding='utf-8') as f:
    json.dump(facility_res, f, ensure_ascii=False, indent=4)