from django.urls import path
from .views import OPENAPIViews


urlpatterns = [
    path('kopis/', OPENAPIViews.as_view()),
]
