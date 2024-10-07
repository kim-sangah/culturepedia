from .models import PerformanceLike, Review
from rest_framework import serializers


class PerformanceLikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = PerformanceLike
        fields = ('performance', 'user')


class ReviewSerializer(serializers.ModelSerializer):
    performance = serializers.ReadOnlyField(source='performance.kopis_id')
    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Review
        fields = ('performance', 'author', 'rating', 'title', 'content', 'created_at', 'updated_at')
        read_only_fields = ('performance', 'author')