from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('이메일을 입력해주세요.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    
    gender_choicse = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    
    # 필수필드: email, password, username  선택필드: gender, birthday
    email = models.EmailField(unique=True)  # email 필드 고유값 설정
    password = models.CharField(max_length=120)
    username = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=gender_choicse, null = True, blank =True)
    birthday = models.DateField(null = True, blank =True)
    
    USERNAME_FIELD = 'email'  # email 유저 식별자 설정
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    def __str__(self):
        return self.username