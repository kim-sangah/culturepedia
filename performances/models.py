from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Performlist(models.Model):
    kopis_id = models.CharField(primary_key=True, max_length=10)
    facility_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, null=True)
    start_date = models.CharField(max_length=20) 
    end_date = models.CharField(max_length=20)
    type = models.CharField(max_length=10)
    state = models.CharField(max_length=10)


class Performance(models.Model):
    kopis_id = models.CharField(primary_key=True, max_length=10)
    title = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=20)
    start_date = models.CharField(max_length=20) 
    end_date = models.CharField(max_length=20)
    facility_kopis_id = models.ForeignKey('Facility', on_delete=models.DO_NOTHING, related_name='performance_facility')
    facility_name = models.CharField(max_length=100)
    type = models.CharField(max_length=10)
    area = models.CharField(max_length=10)
    synopsis = models.TextField(null=True, blank=True)
    cast = models.CharField(max_length=100)
    crew = models.CharField(max_length=100)
    runtime = models.CharField(max_length=10)
    age = models.CharField(max_length=10)
    production = models.CharField(max_length=20)
    agency = models.CharField(max_length=20)
    pricing = models.CharField(max_length=100)
    visit = models.CharField(max_length=2)
    daehakro = models.CharField(max_length=2)
    festival = models.CharField(max_length=2)
    musicallicense = models.CharField(max_length=2)
    musicalcreate = models.CharField(max_length=2)
    dtguidance = models.CharField(max_length=100)
    poster = models.TextField()
    styurl = models.TextField()

    def __str__(self):
        return self.title


class Facility(models.Model):
    kopis_id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)
    seatscale = models.IntegerField()
    relateurl = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    telno = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=20)
    like = models.PositiveIntegerField(default=0) 


class Review(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
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

