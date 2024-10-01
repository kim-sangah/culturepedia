from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    
    gender_choicse = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    #필수필드: email, password, username  선택필드: gender, birthday
    email = models.EmailField(unique=True)  #email 필드 고유값 설정
    password = models.CharField(max_length=120)
    username = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=gender_choicse, default='Other')
    birthday = models.DateField(null = True, blank =True)
    
    USERNAME_FIELD = 'email'  #email 유저 식별자 설정
    REQUIRED_FIELDS = [] 
    
    def __str__(self):
        return self.username