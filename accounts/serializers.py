from .models import User
from rest_framework import serializers
from performances.serializers import PerformanceSerializer, ReviewSerializer


class UserSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    liked_articles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'username', 'gender', 'birthday', 'reviews', 'liked_performance')

    def get_liked_performance(self, obj):
        #각 사용자가 찜한 항목을 performancesLike 모델을 통해 가져와서 목록을 알려준다.
    
        liked_performance = obj.performance_likes.all() #relate_name을 통해 사용자가 찜한 기록을 가져온다.
        performances = [like.performances for like in liked_performance]  # 각 PerformanceLike의 article을 가져옴
        if performances:
            return PerformanceSerializer(performances, many=True).data  # ArticleSerializer로 직렬화
        return 0


class UserModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'username', 'gender', 'birthday')
