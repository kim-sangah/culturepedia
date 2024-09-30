from django.urls import path
from . import views

#API 경로
urlpatterns = [
    path("", views.UserSignupView.as_view()),  #회원가입
    path("delete/", views.UserSignupDelete.as_view()),  #회원탈퇴 
    path("signin/", views.UserLoginView.as_view()),  #로그인
    path("signout/", views.UserSignoutView.as_view()),  #로그아웃
    path("modify/", views.UserModifyView.as_view()),  #회원정보수정
    path("profile/{user.pk}/", views.UserProfileView.as_view()),  #프로필 조회
]
