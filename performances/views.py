from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Performance, Review, PerformanceLike
from .serializers import PerformanceListSerializer, PerformanceDetailSerializer, ReviewSerializer


# 공연 목록 페이지 설정
class PerformancePagination(PageNumberPagination):
    page_size = 100

    def get_paginated_response(self, data):
        return Response({
            '공연수': self.page.paginator.count,
            '총페이지': self.page.paginator.num_pages,
            '현재페이지': self.page.number,
            '공연목록': data,
        })


# 공연 목록 조회
class PerformanceListAPIView(APIView):
    def get(self, request):
        performances = Performance.objects.all()
        paginator = PerformancePagination()
        paginated_performances = paginator.paginate_queryset(performances, request)
        serializer = PerformanceListSerializer(paginated_performances, many=True)
        return paginator.get_paginated_response(serializer.data)


# 공연 검색 
class PerformanceSearchAPIView(APIView):
    def get(self, request):
        query = request.GET.get('keyword')
        performances = Performance.objects.all()

        if query:
            performances = performances.filter(
                Q(title__icontains=query) |  # 공연명
                Q(facility_name__icontains=query) |  # 공연장이름
                Q(crew__icontains=query) |  # 공연제작진
                Q(cast__icontains=query)  # 공연출연진
            )

            if performances.exists():
                paginator = PerformancePagination()
                paginated_performances = paginator.paginate_queryset(performances, request)
                serializer = PerformanceListSerializer(paginated_performances, many=True)
                return paginator.get_paginated_response(serializer.data)

        return Response({"message": "검색된 공연이 없습니다."}, status=status.HTTP_200_OK)


# 공연 상세 조회
class PerformanceDetailAPIView(APIView):
    def get(self, request, pk):
        performance = get_object_or_404(Performance, pk=pk)
        serializer = PerformanceDetailSerializer(performance)
        return Response(serializer.data)


#공연 찜
class PerformanceLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    #공연 찜하기
    def post(self,request,pk):
        performance = get_object_or_404(Performance, pk=pk)
        user = request.user
        
        if PerformanceLike.objects.filter(user=user, performance=performance).exists():
            return Response({"message": "이미 찜한 공연입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        PerformanceLike.objects.create(user=user, performance=performance)
        return Response({"message": "찜한 공연목록에 추가 되었습니다 "}, status=status.HTTP_201_CREATED)

    #공연 찜취소
    def delete(self, request, pk):
        performance = get_object_or_404(Performance, pk=pk)
        user =request.user
        
        like = get_object_or_404(PerformanceLike, user=user, performance=performance)
        like.delete()
        return Response({"message": "찜한 공연목록에서 제외되었습니다"}, status=status.HTTP_200_OK)


# 공연 리뷰 작성
class ReviewCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # 공연 리뷰 작성
    def post(self, request, pk):
        performance = get_object_or_404(Performance, pk=pk)
        serializer = ReviewSerializer(data=request.data)

        if Review.objects.filter(author=request.user, performance=performance).exists():
            return Response({"message": "이미 리뷰를 작성한 공연입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        elif serializer.is_valid():
            serializer.save(performance=performance, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 공연 리뷰 수정 및 삭제
class ReviewAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, review_pk):
        return get_object_or_404(Review, pk=review_pk)
    
    # 공연 리뷰 수정
    def put(self, request, review_pk):
        review = self.get_object(review_pk)

        if review.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = ReviewSerializer(review, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(performance=review.performance, author=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 공연 리뷰 삭제
    def delete(self, request, review_pk):
        review = self.get_object(review_pk)

        if review.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        review.delete()
        return Response({"message": "리뷰가 삭제되었습니다."},status=status.HTTP_204_NO_CONTENT)