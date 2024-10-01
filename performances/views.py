import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated
from django.shortcuts import get_object_or_404
from .models import Article,PerformanceLike
from .serializers import ArticleSerializer
from culturepedia import settings
import xml.etree.ElementTree as ET

API_KEY = settings.API_KEY  # settings에서 API_KEY 불러오기


class OPENAPIViews(APIView):
    
    def get(self, request, *args, **kwargs):
        url = "https://www.kopis.or.kr/openApi/restful/pblprfr"

        params = {
            'service': API_KEY,
            'cpage': '1',
            'rows': '10',
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
                    product_data.append(data)
            except ET.ParseError:
                return Response({'error': 'Failed to parse XML data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # API 요청 실패하면 성공이 아닌 실패로
            return Response({'error': f"Failed to retrieve data. Status code: {response.status_code}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(product_data, status=status.HTTP_200_OK)
    
    
    
#게시글 목록 조회 및 등록
class PerformanceDetail(APIView):
    #게시글등록
    def post(self,request):
        title = request.data.get("title")
        article = Article.objects.create(title=title)
        serializer = ArticleSerializer(article)
        
        # return Response({"message": "게시글 등록완료", "id":article.id},status=status.HTTP_200_OK)
        return Response(serializer.data)
        
    
    #특정 게시글 조회
    def get(self,request,pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
#찜하기 로그인한 사용자만 가능
class PerformanceLikeView(APIView):
    permission_classes = [IsAuthenticated] # 로그인한 사용자만 가능
    
    def post(self,request,pk):
        article = get_object_or_404(Article, pk=pk)
        user = request.user
        
        #이미 찜했는지 확인하기
        
        if PerformanceLike.objects.filter(user=user, article=article).exists():
            return Response({"message":"이미 찜한 공연입니다."},status=status.HTTP_400_BAD_REQUEST)
        
        #찜하기 추가및 like 증가
        PerformanceLike.objects.create(user=user, article=article)
        article.like += 1
        article.save()

        return Response({"message":"찜한 공연목록에 추가 되었습니다 "},status=status.HTTP_201_CREATED)
    
    
    def delete(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        user =request.user
        
        # 찜하기 취소 및 카운트 감소
        like = get_object_or_404(PerformanceLike, user=user, article=article)
        like.delete()

        # if article.like > 0:
        #     article.like -= 1
        #     article.save()
        return Response({"message":"찜한 공연목록에서 제외되었습니다"}, status=status.HTTP_200_OK)