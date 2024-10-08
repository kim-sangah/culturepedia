from .models import User
from rest_framework import serializers
from performances.serializers import PerformanceLikeSerializer, ReviewSerializer


class UserSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    likes = PerformanceLikeSerializer(many=True, source='liked_by')

    class Meta:
        model = User
        fields = ('email', 'username', 'gender', 'birthday', 'reviews', 'likes')

class UserModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'username', 'gender', 'birthday')
