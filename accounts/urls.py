from django.urls import path
from .views import UserSigninView, UserSignoutView


urlpatterns = [
    path('signin/', UserSigninView.as_view()),
    path('signout/', UserSignoutView.as_view()),
]
