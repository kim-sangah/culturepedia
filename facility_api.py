import requests
import json
from culturepedia import config
import xmltodict

api_key = config.API_KEY

performance_res = []

for pageNum in range(1, 50):
    url = f'http://www.kopis.or.kr/openApi/restful/prfplc/{}?service={api_key}'
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


with open('performance_370.json', "w", encoding='utf-8') as f:

    json.dump(performance_res, f, ensure_ascii=False, indent=4)