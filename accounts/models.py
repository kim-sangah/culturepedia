from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    gender_choice = (("M","남성"),("F","여성"))

    email = models.EmailField(max_length=20, unique=True,)
    password = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=gender_choice, null=True, blank=True)
    birthday = models.DateField(auto_now_add=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []