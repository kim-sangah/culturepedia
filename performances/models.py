from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class PerformanceReview(models.Model):
    title = models.CharField(max_length=20)
    like = models.PositiveIntegerField(default=0) 


#찜하기 기능
class PerformanceLike(models.Model):
    article = models.ForeignKey(PerformanceReview, related_name='liked_by', on_delete=models.CASCADE) #사용자가 찜하려고 선택한 게시글 제목
    user = models.ForeignKey(User, related_name='performance_likes', on_delete=models.CASCADE) #로그인한 사용자

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'article'], name='unique_like')
        ]
