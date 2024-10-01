from django.urls import path
from .views import OPENAPIViews


urlpatterns = [
    path('kopis/', OPENAPIViews.as_view()),
    path('kopis/<str:pk>/', OPENAPIViews.as_view()),
]
