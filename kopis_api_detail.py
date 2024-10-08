import requests
import json
import os
import django
import xmltodict
from culturepedia import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'culturepedia.settings')
django.setup()

from performances.models import Performlist, Performance

api_key = config.API_KEY

performancedetail_res = []
existing_ids = set()
performance_ids = list(Performlist.objects.values_list('kopis_id', flat=True))

for performance_code in performance_ids:
    url = f'http://www.kopis.or.kr/openApi/restful/pblprfr/{performance_code}?service={api_key}'
    response = requests.get(url)
    data = xmltodict.parse(response.content)

    db_data = data.get('dbs', {}).get('db', None)

    if isinstance(db_data, dict):
            try:
                mt20id = db_data['mt20id']
                title = db_data['prfnm']
                state = db_data['prfstate']
                start_date = db_data.get('prfpdfrom', 'N/A')
                end_date = db_data.get('prfpdto', 'N/A')
                facility_kopis_id = db_data['mt10id']
                facility_name = db_data.get('fcltynm', 'N/A')
                type = db_data.get('genrenm', 'N/A')
                area = db_data.get('area', 'N/A')
                synopsis = db_data.get('sty', 'N/A')
                cast = db_data.get('prfcast', 'N/A')
                crew = db_data.get('prfcrew', 'N/A')
                runtime = db_data.get('prfruntime', 'N/A')
                age = db_data.get('prfage', 'N/A')
                production = db_data.get('entrpsnmP', 'N/A')
                agency = db_data.get('entrpsnmA', 'N/A')
                pricing = db_data.get('pcseguidance', 'N/A')
                visit = db_data['visit']
                daehakro = db_data['daehakro']
                festival = db_data['festival']
                musicallicense = db_data['musicallicense']
                musicalcreate = db_data['musicalcreate']
                dtguidance = db_data.get('dtguidance', 'N/A')
                poster = db_data.get('poster', 'N/A')
                styurls = db_data.get('styurls', 'N/A')                

                try:
                    performance = Performance.objects.get(kopis_id=mt20id)

                    fields_to_update = {
                        "title": title,
                        "state": state,
                        "start_date": start_date,
                        "end_date": end_date,
                        "facility_kopis_id": facility_kopis_id,
                        "facility_name": facility_name,
                        "type": type,
                        "area": area,
                        "synopsis": synopsis,
                        "cast": cast,
                        "crew": crew,
                        "runtime": runtime,
                        "age": age,
                        "production": production,
                        "agency": agency,
                        "pricing": pricing,
                        "visit": visit,
                        "daehakro": daehakro,
                        "festival": festival,
                        "musicallicense": musicallicense,
                        "musicalcreate": musicalcreate,
                        "dtguidance": dtguidance,
                        "poster": poster,
                        "styurls": styurls,
                    }

                    updated = False

                    for field, new_value in fields_to_update.items():
                        if getattr(performance, field) != new_value:
                            setattr(performance, field, new_value)
                            updated = True
                    
                    if updated:
                        performance.save()
                        print(f'{mt20id}의 정보가 업데이트되었습니다.')

                except Performance.DoesNotExist:
                    performance_dict = {
                    "model": "performances.performance",
                    "pk": db_data['mt20id'],
                    'fields': 
                    {
                        "title": db_data['prfnm'],
                        "state": db_data['prfstate'],
                        "start_date": db_data.get('prfpdfrom', 'N/A'),
                        "end_date": db_data.get('prfpdto', 'N/A'),
                        "facility_kopis_id": db_data['mt10id'],
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
                        "styurls": db_data.get('styurls', 'N/A'),
                    }
                    }
                    performancedetail_res.append(performance_dict)
                    existing_ids.add(mt20id)
            except Exception as e:
                print(f"Error occurred: {e}")
    else:
        pass

folder_path = 'performances/fixtures'
os.makedirs(folder_path, exist_ok=True)

file_path = os.path.join(folder_path, 'performances_detail.json')

with open(file_path, "w", encoding='utf-8') as f:
    json.dump(performancedetail_res, f, ensure_ascii=False, indent=4)