from django.urls import path
from . import views


urlpatterns = [
    path('', views.OPENAPIViews.as_view()),  # 공연 목록 조회
    path('search/', views.PerformanceSearchAPIView.as_view()),  # 공연 검색
    path('detail/<str:pk>/', views.PerformanceDetailAPIView.as_view()),
    path('detail/<str:pk>/like/', views.PerformanceLikeView.as_view()),  # 찜하기 추가 및 취소
    path('detail/<str:pk>/review/', views.ReviewCreateAPIView.as_view()),  # 리뷰 작성
    path('detail/review/<int:review_pk>/', views.ReviewAPIView.as_view()),  # 리뷰 수정 및 삭제
    path('recommend/<int:pk>/', views.RecommendationAPIView.as_view()), # 공연 추천
    path('hashtag/', views.HashtagcreateAPIView.as_view()), # 해시태그 생성
    path('api/user/status/', views.UserStatusView.as_view(), name='user_status'),
    # path('size/<str:pk>/', views.FileSizeViews.as_view()), # 파일 사이즈 체크 테스트용
]
