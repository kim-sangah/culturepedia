from .models import User
from rest_framework import serializers
from performances.models import Article,PerformanceLike
from performances.serializers import ArticleSerializer


class UserSerializer(serializers.ModelSerializer):
    liked_articles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'username', 'gender', 'birthday', 'liked_articles')

    def get_liked_articles(self, obj):
        liked_articles = obj.performance_likes.all() #relate_name을 통해 사용자가 찜한 기록을 가져온다.
        articles = [like.article for like in liked_articles]  # 각 PerformanceLike의 article을 가져옴
        if articles:
            return ArticleSerializer(articles, many=True).data  # ArticleSerializer로 직렬화
        return []
    
    
    
class UserModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'username', 'gender', 'birthday')
