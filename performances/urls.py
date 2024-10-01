from django.urls import path
from .views import OPENAPIViews,PerformanceDetail,ArticleLikeView
from .import views


urlpatterns = [
    path('kopis/', OPENAPIViews.as_view()),
    path('detail/', views.PerformanceDetail.as_view()),  # 게시글 등록 (POST)
    path('detail/<int:pk>/', views.PerformanceDetail.as_view()),  # 게시글 조회 (GET)
    path('detail/<int:pk>/like/', views.ArticleLikeView.as_view()),  # 찜하기 추가 및 취소
    
]
