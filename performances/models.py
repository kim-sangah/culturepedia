from django.db import models

# Create your models here.
class Performance(models.Model):
    facility_id = models.ForeignKey('Facility',on_delete=models.CASCADE, null=True) #외래키 참조
    title = models.CharField(max_length=100, null=True )
    
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
    