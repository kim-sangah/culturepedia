import requests
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Performance, Review, PerformanceLike
from .serializers import ReviewSerializer
from culturepedia import settings
import xml.etree.ElementTree as ET
from datetime import datetime
from openai import OpenAI
from django.conf import settings
from django.db.models import Q
from .bots import generate_synopsis, generate_hashtags_for_performance, generate_recommendations, generate_recommendations_with_tags


API_KEY = settings.API_KEY  # settings에서 API_KEY 불러오기


class OPENAPIViews(APIView):
    def get(self, request, *args, **kwarg):
        # 공연 목록 조회
        performance_list = self.get_ticket_sales()
        if performance_list is not None:
            return Response(performance_list, status=status.HTTP_200_OK)
        else:
            return Response({'error': '공연 목록을 불러오지 못했습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_ticket_sales(self):
        # 예매상황판 (유료 공연 티켓 판매율 기준으로 집계됨) 조회
        url = "https://www.kopis.or.kr/openApi/restful/boxoffice"
        params = {
            'service': API_KEY,  # 필수
            'ststype': 'week',  # 필수
            'date': '20240830',  # 필수
            'catecode': 'GGGA',
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            try:
                root = ET.fromstring(response.content)
                sales_data = []
                for item in root.findall('boxof'):
                    data = {
                        '공연명': item.find('prfnm').text if item.find('prfnm') is not None else None,
                        '장르': item.find('cate').text if item.find('cate') is not None else None,
                        '순위': int(item.find('rnum').text) if item.find('rnum') is not None else None,
                        '공연기간': item.find('prfpd').text if item.find('prfpd') is not None else None,
                        '공연장': item.find('prfplcnm').text if item.find('prfplcnm') is not None else None,
                        '좌석수': item.find('seatcnt').text if item.find('seatcnt') is not None else None,
                        '포스터': item.find('poster').text if item.find('poster') is not None else None,
                    }
                    sales_data.append(data)
                sales_data = sorted(sales_data, key=lambda x: x['순위'])
                return sales_data
            except ET.ParseError:
                return Response({'error': 'Failed to parse XML data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OPENAPIDetailViews(APIView):
    
    def get(self, request, *args, **kwargs):
        performance_id = kwargs.get('pk')
        if performance_id:
            # 공연 상세 정보 조회
            performance_data = self.get_performance_details(performance_id)
            if performance_data is not None:
                # 공연장소정보를 받아 공연 세부 정보에 추가함
                facility_id = performance_data.get('공연시설아이디')
                if facility_id:
                    facility_data = self.get_facility_details(facility_id)
                    if facility_data is not None:
                        performance_data['공연장소정보'] = facility_data
                    else:
                        return Response({'error': '공연 장소 상세 정보를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
                return Response(performance_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': '공연 상세 정보를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # 공연 목록 조회
            performance_list = self.get_ticket_sales()
            if performance_list is not None:
                return Response(performance_list, status=status.HTTP_200_OK)
            else:
                return Response({'error': '공연 목록을 불러오지 못했습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_performance_details(self, performance_id):
        url = f"https://www.kopis.or.kr/openApi/restful/pblprfr/{performance_id}"
        params = {'service': API_KEY, 'mt20id': performance_id}
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
                        '공연시간': item.find('dtguidance').text if item.find('dtguidance') is not None else None,
                    }
                    # performance_data의 '소개이미지목록'에 있는 소개이미지들을 list로 저장
                    styurls_element = item.find('styurls')
                    if styurls_element is not None:
                        images = [
                            styurl.text for styurl in styurls_element.findall('styurl')]
                        performance_data['소개이미지목록'] = images
                    return performance_data
            except ET.ParseError:
                return Response({'error': 'Failed to parse XML data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'error': f"Failed to retrieve data. Status code: {response.status_code}"}, status=status.HTTP_400_BAD_REQUEST)

    def get_facility_details(self, facility_id):
        url = f"https://www.kopis.or.kr/openApi/restful/prfplc/{facility_id}"
        params = {'service': API_KEY, 'mt10id': facility_id}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            try:
                root = ET.fromstring(response.content)
                item = root.find('db')
                if item is not None:
                    facility_data = {
                        '공연시설명': item.find('fcltynm').text if item.find('fcltynm') is not None else None,
                        '좌석수': item.find('seatscale').text if item.find('seatscale') is not None else None,
                        '홈페이지': item.find('relateurl').text if item.find('relateurl') is not None else None,
                        '주소': item.find('adres').text if item.find('adres') is not None else None,
                        '전화번호': item.find('telno').text if item.find('telno') is not None else None,
                    }
                    return facility_data
            except ET.ParseError:
                return Response({'error': 'Failed to parse XML data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'error': '공연 장소 상세 정보를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)


class OPENAPISearchViews(APIView):

    # 전체 조회 및 검색(공연명, 공연시설명, 제작사, 출연진)
    def get(self, request, *args, **kwargs):

        search = kwargs.get('pk', None)

        lookup_url = f"https://www.kopis.or.kr/openApi/restful/pblprfr/"

        now_date = datetime.now().strftime('%Y%m%d')

        stdate = request.GET.get('stdate', '20240101')
        eddate = request.GET.get('eddate', now_date)
        cpage = request.GET.get('cpage', '1')

        params = {
            'service': API_KEY,
            'stdate': stdate,
            'eddate': eddate,
            'cpage': cpage,
            'rows': '10',
        }

        if search:
            params['rows'] = 50

        # 외부 API 호출
        response = requests.get(lookup_url, params=params)

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
                    mt20id = item.find('mt20id').text if item.find(
                        'mt20id') is not None else None

                    detail_url = f"{lookup_url}/{mt20id}?service={API_KEY}"

                    detail_response = requests.get(detail_url)

                    detail_root = ET.fromstring(detail_response.content)

                    prfcrew_elem = detail_root.find('.//prfcrew')
                    prfcast_elem = detail_root.find('.//prfcast')
                    prfcrew = prfcrew_elem.text if prfcrew_elem is not None else None
                    prfcast = prfcast_elem.text if prfcast_elem is not None else None

                    if search:
                        if not (search in title or search in facility_name or search in prfcrew or search in prfcast):
                            continue

                    data = {
                        '공연ID': mt20id,
                        '공연명': title,
                        '장르': item.find('genrenm').text if item.find('genrenm') is not None else None,
                        '공연상태': item.find('prfstate').text if item.find('prfstate') is not None else None,
                        '공연시작일': item.find('prfpdfrom').text if item.find('prfpdfrom') is not None else None,
                        '공연종료일': item.find('prfpdto').text if item.find('prfpdto') is not None else None,
                        '포스터': item.find('poster').text if item.find('poster') is not None else None,
                        '공연장명': facility_name,
                        '오픈런': item.find('openrun').text if item.find('openrun') is not None else None,
                        '공연지역': item.find('area').text if item.find('area') is not None else None,
                        '제작사': prfcrew,
                        '출연진': prfcast,
                    }
                    product_data.append(data)

            except ET.ParseError:
                return Response({'error': 'Failed to parse XML data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # API 요청 실패하면 성공이 아닌 실패로
            return Response({'error': f"Failed to retrieve data. Status code: {response.status_code}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(product_data, status=status.HTTP_200_OK)



# #게시글 목록 조회 및 등록
# class PerformanceDetail(APIView):
#     #게시글등록
#     def post(self, request):
#         title = request.data.get("title")
#         article = Article.objects.create(title=title)
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)
    
#     #특정 게시글 조회
#     def get(self, request, pk):
#         article = get_object_or_404(Article, pk=pk)
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data, status=status.HTTP_200_OK)


#공연 찜
class PerformanceLikeView(APIView):
    permission_classes = [IsAuthenticated]

    #공연 찜하기
    def post(self,request,pk):
        performance = get_object_or_404(Performance, pk=pk)
        user = request.user
        
        #이미 찜했는지 확인하기
        if PerformanceLike.objects.filter(user=user, performance=performance).exists():
            return Response({"message": "이미 찜한 공연입니다."},status=status.HTTP_400_BAD_REQUEST)
        
        #찜하기 및 카운트 증가
        PerformanceLike.objects.create(user=user, performance=performance)
        # article.like += 1
        # article.save()
        return Response({"message": "찜한 공연목록에 추가 되었습니다 "},status=status.HTTP_201_CREATED)

    #공연 찜 취소
    def delete(self, request, pk):
        performance = get_object_or_404(Performance, pk=pk)
        user =request.user
        
        like = get_object_or_404(PerformanceLike, user=user, performance=performance)
        like.delete()
        return Response({"message": "찜한 공연목록에서 제외되었습니다"}, status=status.HTTP_200_OK)


#공연 리뷰
class ReviewCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    #공연 리뷰 작성
    def post(self, request, pk):
        performance = get_object_or_404(Performance, pk=pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(performance=performance, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, review_pk):
        return get_object_or_404(Review, pk=review_pk)
    
    #공연 리뷰 수정
    def put(self, request, review_pk):
        review = self.get_object(review_pk)
        if review.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #공연 리뷰 삭제
    def delete(self, request, review_pk):
        comment = self.get_object(review_pk)
        if comment.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response({"message": "리뷰가 삭제되었습니다."},status=status.HTTP_204_NO_CONTENT)
    

# OPENAI API 사용한 공연 추천
class RecommendationAPIView(APIView):
    def post(self, request):
        # 요청을 보낸 사용자가 별점 4점 이상으로 평가하거나 찜한 공연 받아오기
        user_preferences = self.get_user_preferences(request.user)

        # 유저가 입력한 태그 받아오기
        input_tags = request.data.get('input_tags')

        if user_preferences:
            for performance in user_preferences:
                # synopsis가 없는 공연의 synopsis를 OpenAI API로 생성
                # if performance.synopsis:
                #     # synopsis가 있지만 공연에 대한 hashtag가 없다면 OpenAI API로 생성
                #     if performance.performance_hashtag:
                #         continue
                #     else:
                #         generate_hashtags_for_performance(performance)
                # else:
                #     generate_synopsis(performance)
                #     # 공연에 대한 hashtag가 없다면 OpenAI API로 생성
                #     if performance.performance_hashtag:
                #         continue
                #     else:
                #         generate_hashtags_for_performance(performance)
                
                # 공연에 대한 hashtag가 없다면 OpenAI API로 생성
                if performance.performance_hashtag:
                    continue
                else:
                    generate_hashtags_for_performance(performance)
                    
            recommendations = generate_recommendations(user_preferences, input_tags)
        else: # 요청을 보낸 사용자가 리뷰하거나 찜한 공연이 없을 때
            recommendations = generate_recommendations_with_tags(input_tags)

        return Response({"recommendations": recommendations}, status=200)
    
    def get_user_preferences(self, user):
        # 사용자가 별점 4점 이상으로 평가하거나 찜한 공연 불러오기
        reviews = Review.objects.filter(Q(rating__gte=4) & Q(author=user)).values_list('performance_id', flat=True)
        likes = PerformanceLike.objects.filter(user=user).values_list('performance_id', flat=True)

        # Set로 리뷰하거나 찜한 공연의 id가 중복되지 않게 저장
        performance_ids = set(reviews) | set(likes)  # Union of both sets

        # performance_ids에 맞는 Performance object를 받음
        user_preferences = Performance.objects.filter(kopis_id__in=performance_ids)

        return user_preferences
    