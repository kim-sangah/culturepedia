import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from culturepedia import settings
import xml.etree.ElementTree as ET
from datetime import datetime

API_KEY = settings.API_KEY  # settings에서 API_KEY 불러오기


class OPENAPIViews(APIView):

    def get(self, request, *args, **kwargs):
        now_date = datetime.now().strftime('%Y%m%d')

        url = "https://www.kopis.or.kr/openApi/restful/pblprfr"

        stdate = request.GET.get('stdate', '20160101')
        eddate = request.GET.get('eddate', now_date)
        cpage = request.GET.get('cpage', '1')
        prfplccd = request.GET.get('prfplccd', None)
        search = request.GET.get('search', None)

        params = {
            'service': API_KEY,
            'stdate': stdate,
            'eddate': eddate,
            'cpage': cpage,
            'rows': '10',
            'prfplccd': prfplccd,
        }

        # 외부 API 호출
        response = requests.get(url, params=params)

        if response.status_code == 200:
            try:
                # XML 데이터를 파싱
                root = ET.fromstring(response.content)

                # XML 데이터를 Python 딕셔너리로 변환
                product_data = []
                for item in root.findall('db'):  # XML 구조에 맞게 태그명 조정
                    title = item.find('prfnm').text if item.find(
                        'prfnm') is not None else None
                    facility_name = item.find('fcltynm').text if item.find(
                        'fcltynm') is not None else None

                    if search:
                        if not (search in title or search in facility_name):
                            continue

                    data = {
                        '공연ID': item.find('mt20id').text if item.find('mt20id') is not None else None,
                        '공연명': title,
                        '장르': item.find('genrenm').text if item.find('genrenm') is not None else None,
                        '공연상태': item.find('prfstate').text if item.find('prfstate') is not None else None,
                        '공연시작일': item.find('prfpdfrom').text if item.find('prfpdfrom') is not None else None,
                        '공연종료일': item.find('prfpdto').text if item.find('prfpdto') is not None else None,
                        '포스터': item.find('poster').text if item.find('poster') is not None else None,
                        '공연장명': facility_name,
                        '오픈런': item.find('openrun').text if item.find('openrun') is not None else None,
                        '공연지역': item.find('area').text if item.find('area') is not None else None,
                    }
                    product_data.append(data)
            except ET.ParseError:
                return Response({'error': 'Failed to parse XML data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # API 요청 실패하면 성공이 아닌 실패로
            return Response({'error': f"Failed to retrieve data. Status code: {response.status_code}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(product_data, status=status.HTTP_200_OK)
