from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Article(models.Model):
    title = models.CharField(max_length=20)
    like = models.PositiveIntegerField(default=0) 


class Review(models.Model):
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


#찜하기 기능
class PerformanceLike(models.Model):
    article = models.ForeignKey(Article, related_name='liked_by', on_delete=models.CASCADE) #사용자가 찜하려고 선택한 게시글 제목
    user = models.ForeignKey(User, related_name='performance_likes', on_delete=models.CASCADE) #로그인한 사용자

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'article'], name='unique_like')
        ]

