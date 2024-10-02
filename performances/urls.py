from django.urls import path
from . import views


urlpatterns = [
    path('kopis/', views.OPENAPIViews.as_view()),
    path('detail/', views.PerformanceDetail.as_view()),  # 게시글 등록
    path('detail/<int:pk>/', views.PerformanceDetail.as_view()),  # 게시글 조회
    path('detail/<int:pk>/like/', views.PerformanceLikeView.as_view()),  # 찜하기 추가 및 취소

]
