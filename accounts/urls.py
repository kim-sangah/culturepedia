# accounts/urls.py
from django.urls import path
from .views import UserSignupView,UserSignupDelete,UserLoginView

# 회원가입과 회원탈퇴 API 경로
urlpatterns = [
    path("", UserSignupView.as_view()),  # 회원가입
    path("delete/", UserSignupDelete.as_view()),  # 회원탈퇴 
    # path("login/", UserLoginView.as_view()), #로그인

    

]
