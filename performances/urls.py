from django.urls import path
from . import views


urlpatterns = [
    path('', views.PerformanceListAPIView.as_view()),
    path('search/', views.PerformanceSearchAPIView.as_view()),
    path('<str:pk>/', views.PerformanceDetailAPIView.as_view()),
    path('<str:pk>/like/', views.PerformanceLikeAPIView.as_view()),  # 찜하기 추가 및 취소
    path('<str:pk>/review/', views.ReviewCreateAPIView.as_view()),  # 리뷰 작성
    path('review/<int:review_pk>/', views.ReviewAPIView.as_view()),  # 리뷰 수정 및 삭제
]
