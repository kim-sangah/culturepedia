from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Facility(models.Model):
    name = models.CharField(max_length=100)
    seatscale = models.IntegerField()
    relateurl = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    telno = models.CharField(max_length=20)


class Performance(models.Model):
    facility_id = models.ForeignKey('Facility',on_delete=models.CASCADE, null=False) #외래키 참조
    title = models.CharField(max_length=100, null=False )
    
    #공연시작날짜만 들어감
    start_date = models.DateField() 
    end_date = models.DateField()
    cast = models.CharField(max_length=10)
    crew = models.CharField(max_length=10)
    runtime = models.IntegerField(null= True)
    age = models.IntegerField()
    entprsmnP = models.CharField(max_length=100)
    entrprsnmA = models.CharField(max_length=100)
    pricing = models.IntegerField()# 가격
    
    poster = models.ImageField(upload_to="") #일단 경로는 빈칸
    synopsis = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    visit = models.BooleanField(default=False)
    daehakro = models.BooleanField(default=False)
    festival = models.BooleanField(default=False)
    musicallicense = models.BooleanField(default=False)
    musicalcreate = models.BooleanField(default=False)
    dtguidance = models.CharField(max_length=100)



class PerformanceReview(models.Model):
    title = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    # like = models.PositiveIntegerField(default=0)


#찜하기 기능
class PerformanceLike(models.Model):
    user = models.ForeignKey(User, related_name='performance_likes', on_delete=models.CASCADE) #로그인한 사용자
    article = models.ForeignKey(PerformanceReview, related_name='liked_by', on_delete=models.CASCADE) #사용자가 찜하려고 선택한 게시글 제목

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'article'], name='unique_like')
        ]
