from django.urls import path
from . import views


urlpatterns = [
    path('kopis/', views.OPENAPIViews.as_view()),
    path('kopis/search/<str:pk>/', views.OPENAPISearchViews.as_view()),
    path('kopis/<str:pk>/', views.OPENAPIDetailViews.as_view()),
    path('detail/<str:pk>/like/', views.PerformanceLikeView.as_view()),  # 찜하기 추가 및 취소
    path('detail/<str:pk>/review/', views.ReviewCreateAPIView.as_view()),  # 리뷰 작성
    path('detail/review/<int:review_pk>/', views.ReviewAPIView.as_view()),  # 리뷰 수정 및 삭제
    path('recommend/<int:pk>/', views.RecommendationAPIView.as_view()), # 공연 추천
    path('size/<str:pk>/', views.FileSizeViews.as_view()), # 파일 사이즈 체크 테스트용
]
