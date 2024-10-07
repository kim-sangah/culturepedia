from .models import Performance, Review
from rest_framework import serializers


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ('id', 'title', 'like')


class ReviewSerializer(serializers.ModelSerializer):
    performance = serializers.ReadOnlyField(source='performance.kopis_id')
    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Review
        fields = ('performance', 'author', 'rating', 'title', 'content', 'created_at', 'updated_at')
        read_only_fields = ('performance', 'author')