from .models import Article, Review
from rest_framework import serializers


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('__all__',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Review
        fields = ('article_id', 'rating', 'title', 'content', 'created_at', 'updated_at')
        read_only_fields = ('article_id',)