from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):

        if not email:
            raise ValueError('이메일을 입력해주세요')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    gender_choice = (("M","남성"),("F","여성"))

    email = models.EmailField(max_length=20, unique=True,)
    password = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=gender_choice, null=True, blank=True)
    birthday = models.DateField(auto_now_add=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'