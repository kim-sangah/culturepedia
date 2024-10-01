import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from culturepedia import settings
import xml.etree.ElementTree as ET

API_KEY = settings.API_KEY  # settings에서 API_KEY 불러오기


class OPENAPIViews(APIView):

    def get(self, request, *args, **kwargs):
        performance_id = kwargs.get('pk')
        if performance_id:
            # 공연 상세 정보 요청
            url = f"https://www.kopis.or.kr/openApi/restful/pblprfr/{performance_id}"
            params = {
                'service': API_KEY,
                'mt20id': performance_id,
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                try:
                    root = ET.fromstring(response.content)
                    item = root.find('db')
                    if item is not None:
                        performance_data = {
                            '공연명': item.find('prfnm').text if item.find('prfnm') is not None else None,
                            '공연시설아이디': item.find('mt10id').text if item.find('mt10id') is not None else None,
                            '공연시작일': item.find('prfpdfrom').text if item.find('prfpdfrom') is not None else None,
                            '공연종료일': item.find('prfpdto').text if item.find('prfpdto') is not None else None,
                            '공연장명': item.find('fcltynm').text if item.find('fcltynm') is not None else None,
                            '공연출연진': item.find('prfcast').text if item.find('prfcast') is not None else None,
                            '공연제작진': item.find('prfcrew').text if item.find('prfcrew') is not None else None,
                            '런타임': item.find('prfruntime').text if item.find('prfruntime') is not None else None,
                            '관람연령': item.find('prfage').text if item.find('prfage') is not None else None,
                            '제작사': item.find('entrpsnmP').text if item.find('entrpsnmP') is not None else None,
                            '기획사': item.find('entrpsnmA').text if item.find('entrpsnmA') is not None else None,
                            '티켓가격': item.find('pcseguidance').text if item.find('pcseguidance') is not None else None,
                            '포스터': item.find('poster').text if item.find('poster') is not None else None,
                            '줄거리': item.find('sty').text if item.find('sty') is not None else None,  
                            '장르': item.find('genrenm').text if item.find('genrenm') is not None else None,
                            '공연상태': item.find('prfstate').text if item.find('prfstate') is not None else None,
                            '내한': item.find('visit').text if item.find('visit') is not None else None,
                            '대학로': item.find('daehakro').text if item.find('daehakro') is not None else None,
                            '축제': item.find('festival').text if item.find('festival') is not None else None,
                            '뮤지컬라이센스': item.find('musicallicense').text if item.find('musicallicense') is not None else None,
                            '뮤지컬창작': item.find('musicalcreate').text if item.find('musicalcreate') is not None else None,
                        }

                        # performance_data의 '소개이미지목록'에 있는 소개이미지들을 list로 저장
                        styurls_element = item.find('styurls')
                        if styurls_element is not None:
                            # 'styurls'에 있는 'styurl' 요소를 iterate함
                            images = [styurl.text for styurl in styurls_element.findall('styurl') if styurl is not None]
                            performance_data['소개이미지목록'] = images
                        else:
                            performance_data['소개이미지목록'] = []

                        # performance_data의 '공연시설아이디'로 공연시설 상세 정보를 요청
                        facility_id = item.find('mt10id').text
                        if facility_id:
                            facility_url = f"https://www.kopis.or.kr/openApi/restful/prfplc/{facility_id}"
                            facility_params = {'service': API_KEY, 'mt10id': facility_id}
                            facility_response = requests.get(facility_url, params=facility_params)

                            if facility_response.status_code == 200:
                                facility_root = ET.fromstring(facility_response.content)
                                facility_item = facility_root.find('db')
                                if facility_item is not None:
                                    location_data = {
                                        '공연시설명': facility_item.find('fcltynm').text if facility_item.find('fcltynm') is not None else None,
                                        '좌석수': facility_item.find('seatscale').text if facility_item.find('seatscale') is not None else None,
                                        '홈페이지': facility_item.find('relateurl').text if facility_item.find('relateurl') is not None else None,
                                        '주소': facility_item.find('adres').text if facility_item.find('adres') is not None else None,
                                        '전화번호': facility_item.find('telno').text if facility_item.find('telno') is not None else None,
                                    }
                                    performance_data['공연장소정보'] = location_data
                                else:
                                    return Response({'error': '공연 장소 상세 정보를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
                            else:
                                return Response({'error': f"공연 장소 상세 정보를 불러오지 못했습니다. Status code: {facility_response.status_code}"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'error': '공연 상세 정보를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

                except ET.ParseError:
                    return Response({'error': 'Failed to parse XML data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(performance_data, status=status.HTTP_200_OK)
        else:
            # 공연 목록 요청
            url = "https://www.kopis.or.kr/openApi/restful/pblprfr"
            params = {
                'service': API_KEY,
                'cpage': '1',
                'rows': '10',
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                try:
                    root = ET.fromstring(response.content)
                    performance_list = []
                    for item in root.findall('db'):
                        data = {
                            '공연명': item.find('prfnm').text if item.find('prfnm') is not None else None,
                            '공연시작일': item.find('prfpdfrom').text if item.find('prfpdfrom') is not None else None,
                            '공연종료일': item.find('prfpdto').text if item.find('prfpdto') is not None else None,
                            '공연장명': item.find('fcltynm').text if item.find('fcltynm') is not None else None,
                            '포스터': item.find('poster').text if item.find('poster') is not None else None,
                            '공연지역': item.find('area').text if item.find('area') is not None else None,
                            '장르': item.find('genrenm').text if item.find('genrenm') is not None else None,
                            '오픈런': item.find('openrun').text if item.find('openrun') is not None else None,
                            '공연상태': item.find('prfstate').text if item.find('prfstate') is not None else None,
                        }
                        performance_list.append(data)
                    return Response(performance_list, status=status.HTTP_200_OK)
                except ET.ParseError:
                    return Response({'error': 'Failed to parse XML data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                # API 요청 실패하면 성공이 아닌 실패로
                return Response({'error': f"Failed to retrieve data. Status code: {response.status_code}"}, status=status.HTTP_400_BAD_REQUEST)
