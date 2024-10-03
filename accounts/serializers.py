from .models import User
from rest_framework import serializers
from performances.serializers import ArticleSerializer


class UserSerializer(serializers.ModelSerializer):
    liked_articles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'username', 'gender', 'birthday','liked_articles')

    def get_liked_articles(self, obj):
        # 각 사용자가 찜한 항목을 PerformanceLike 모델을 통해 가져와서 목록을 알려줌
        liked_articles = obj.performance_likes.all()  # related_name을 통해 사용자가 찜한 기록을 가져옴
        articles = [like.article for like in liked_articles]  # 각 PerformanceLike의 article을 가져옴
        
        # 공연 정보 출력용 데이터 생성
        result = []
        for article in articles:
            performance_data = {
                "performance_id": article.id,
                "title": article.title,
                "date": article.created_at.date()  # 날짜만 출력
            }
            result.append(performance_data)
        
        return result if result else 0
    
class UserModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'username', 'gender', 'birthday')
