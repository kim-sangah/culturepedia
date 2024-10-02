from django.urls import path
from .views import OPENAPIViews, OPENAPISearchViews, OPENAPIDetailViews


urlpatterns = [
    path('kopis/', OPENAPIViews.as_view()),
    path('kopis/search/<str:pk>/', OPENAPISearchViews.as_view()),
    path('kopis/<str:pk>/', OPENAPIDetailViews.as_view()),
]
