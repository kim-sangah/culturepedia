from django.urls import path
from . import views


urlpatterns = [
    path('', views.OPENAPIViews.as_view()),  # 공연 목록 조회
    path('search/', views.PerformanceSearchAPIView.as_view()),  # 공연 검색
    path('<str:pk>/', views.PerformanceDetailAPIView.as_view()),  # 공연 상세 조회
    path('<str:pk>/like/', views.PerformanceLikeAPIView.as_view()),  # 찜하기 및 찜취소
    path('<str:pk>/review/', views.ReviewCreateAPIView.as_view()),  # 리뷰 작성
    path('review/<int:review_pk>/', views.ReviewAPIView.as_view()),  # 리뷰 수정 및 삭제
]
