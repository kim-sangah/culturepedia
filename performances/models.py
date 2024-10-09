from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Hashtag(models.Model):
    performance_api_id = models.ForeignKey(
        'Performance', on_delete=models.CASCADE, related_name='performance_hashtag')
    name = models.CharField(max_length=10)


class Performlist(models.Model):
    kopis_id = models.CharField(primary_key=True, max_length=10)
    facility_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, null=True)
    start_date = models.CharField(max_length=20) 
    end_date = models.CharField(max_length=20)
    type = models.CharField(max_length=10)
    state = models.CharField(max_length=10)


class Performance(models.Model):
    kopis_id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=20)
    start_date = models.CharField(max_length=100) 
    end_date = models.CharField(max_length=100)
    facility_kopis_id = models.ForeignKey(
        'Facility', on_delete=models.DO_NOTHING, related_name='performance_facility')
    facility_name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    synopsis = models.TextField(null=True, blank=True)
    cast = models.CharField(max_length=100, null=True)
    crew = models.CharField(max_length=100, null=True)
    runtime = models.CharField(max_length=100, null=True)
    age = models.CharField(max_length=100, null=True)
    production = models.CharField(max_length=200, null=True)
    agency = models.CharField(max_length=200, null=True)
    pricing = models.TextField(null=True)
    visit = models.CharField(max_length=2)
    daehakro = models.CharField(max_length=2)
    festival = models.CharField(max_length=2)
    musicallicense = models.CharField(max_length=2)
    musicalcreate = models.CharField(max_length=2)
    dtguidance = models.TextField(null=True)
    poster = models.TextField(null=True)
    styurls = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.title


class Facility(models.Model):
    kopis_id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=200)
    seatscale = models.IntegerField(null=True)
    relateurl = models.TextField(null=True)
    address = models.TextField(null=True)
    telno = models.CharField(max_length=200, null=True)


class Review(models.Model):
    performance = models.ForeignKey(
        Performance, on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PerformanceLike(models.Model):
    user = models.ForeignKey(
        User, related_name='liked_by', on_delete=models.CASCADE)
    performance = models.ForeignKey(
        Performance, related_name='performance_likes', on_delete=models.CASCADE)