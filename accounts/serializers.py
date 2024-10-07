from .models import User
from rest_framework import serializers
from performances.models import PerformanceLike
from performances.serializers import PerformanceLikeSerializer, ReviewSerializer


class UserSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    performance_likes = serializers.SerializerMethodField()

    def get_performance_likes(self, obj):
        performance_likes = obj.performance_likes.all()
        return PerformanceLikeSerializer(performance_likes, many=True).data
    
    class Meta:
        model = User
        fields = ('email', 'username', 'gender', 'birthday', 'reviews', 'performance_likes')


class UserModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'username', 'gender', 'birthday')
