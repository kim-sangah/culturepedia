from django.urls import path
from . import views


urlpatterns = [
    path("", views.UserSignupView.as_view()),  # 회원가입
    path("signin/", views.UserSigninView.as_view()),  # 로그인
    path("signout/", views.UserSignoutView.as_view()),  # 로그아웃
    path("profile/<int:pk>/", views.UserProfileView.as_view()),  # 프로필 조회, 수정, 회원탈퇴
]
