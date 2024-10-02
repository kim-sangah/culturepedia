from .models import PerformanceReview
from rest_framework import serializers


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceReview
        fields = ('id', 'title', 'like')