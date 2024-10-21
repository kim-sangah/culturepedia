from .models import User
from rest_framework import serializers
from performances.models import Performance
from performances.serializers import PerformanceListSerializer, ReviewSerializer
import re


class UserSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    likes = serializers.SerializerMethodField()
    birthday = serializers.DateField(required=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'gender', 'birthday', 'reviews', 'likes')
    
    def get_likes(self, obj):
        likes = Performance.objects.filter(performance_likes__user=obj)
        return PerformanceDetailSerializer(likes, many=True).data


class UserModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'username', 'gender', 'birthday')
