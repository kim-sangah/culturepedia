from .models import Performance, Review
from rest_framework import serializers


class PerformanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ('title', 'type', 'facility_name', 'poster', 'start_date', 'end_date')


class ReviewSerializer(serializers.ModelSerializer):
    performance = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ('performance', 'author', 'rating', 'title', 'content', 'created_at', 'updated_at')
        read_only_fields = ('performance', 'author')


class PerformanceDetailSerializer(serializers.ModelSerializer):
    perform_reviews = ReviewSerializer(many=True)

    class Meta:
        model = Performance
        fields = '__all__'