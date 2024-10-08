from .models import Performance, PerformanceLike, Review
from rest_framework import serializers


class PerformanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ('title', 'type', 'facility_name', 'poster', 'start_date', 'end_date')


class PerformanceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = '__all__'


class PerformanceLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceLike
        fields = ('user', 'performance')


class ReviewSerializer(serializers.ModelSerializer):
    performance = serializers.ReadOnlyField(source='performance.kopis_id')
    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Review
        fields = ('performance', 'author', 'rating', 'title', 'content', 'created_at', 'updated_at')
        read_only_fields = ('performance', 'author')