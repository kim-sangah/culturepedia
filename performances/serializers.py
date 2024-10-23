from .models import Performance, Review
from rest_framework import serializers


class PerformanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ('kopis_id', 'title', 'type', 'facility_name',
                  'poster', 'start_date', 'end_date')


class ReviewSerializer(serializers.ModelSerializer):
    performance = serializers.StringRelatedField()
    author = serializers.StringRelatedField()
    author_id = serializers.PrimaryKeyRelatedField(
        source='author', read_only=True)

    class Meta:
        model = Review
        fields = ('performance', 'author', 'author_id', 'rating',
                  'title', 'content', 'created_at', 'updated_at', 'id')
        read_only_fields = ('performance', 'author', 'author_id')


class PerformanceDetailSerializer(serializers.ModelSerializer):
    perform_reviews = ReviewSerializer(many=True)

    class Meta:
        model = Performance
        fields = '__all__'
