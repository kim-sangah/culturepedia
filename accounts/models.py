from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    
    gender = [
        ('M', '남성'),
        ('F', '여성'),
    ]
    #필수필드: email, password, username  선택필드: gender, birthday
    email = models.EmailField(unique=True) #email 필드를 고유값으로 설정
    password = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=gender, null=True, blank=True)
    birthday = models.DateField(null = True, blank =True)
    
    USERNAME_FIELD = 'email' #이메일을 사용자 식별자로 설정
    REQUIRED_FIELDS = [] 
    
    def __str__(self):
        return self.username