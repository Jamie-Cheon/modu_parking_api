from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from lots.models import Lot


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of username.
    A manager is an interface through which database query operations are provided to Django models.
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, username and password.
        """
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)




class User(AbstractUser):
    """
    Use an email address as the primary user identifier instead of a username for authentication
    """
    email = models.EmailField(max_length=100, unique=True, verbose_name='email')
    username = models.CharField(max_length=30, blank=True)
    phoneNum = models.CharField(max_length=20, default='', blank=True, null=True)
    plateNum = models.CharField(max_length=20, default=None, blank=True, null=True)
    cardNum = models.CharField(max_length=20, default=None, blank=True, null=True)
    points = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    # https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#extending-the-existing-user-models
    # 개인정보 암호화 필수 인데 복호화 가능 하게 할지 불가능 하게 할지 서비스 기능에 따라서 결정
    # 자주사용 하는 모델 필드는 Abstract Model 추출
    # https://docs.djangoproject.com/en/3.0/topics/db/models/#abstract-base-classes

    objects = UserManager()  # Replace the default model manager with custom UserManager
    USERNAME_FIELD = 'email'  # Set the USERNAME_FIELD (which defines the unique identifier for the User model) to email
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        is_created = self.id is None

        if is_created:
            self.set_password(self.password)

        user = super().save(*args, **kwargs)

        return user


# class Profile(models.Model):
#     user = models.OneToOneField('users.User', on_delete=models.CASCADE)
#     phone_num = models.CharField(max_length=20, default='', blank=True)
#     plate_num = models.CharField(max_length=20, default=None, blank=True)
#     card_num = models.CharField(max_length=20, default=None, blank=True)
#     points = models.IntegerField(null=True, blank=True)
#
#     @receiver(post_save, sender=User)
#     def create_user_profile(sender, instance, created, **kwargs):
#         if created:
#             Profile.objects.create(user=instance)
#
#     @receiver(post_save, sender=User)
#     def save_user_profile(sender, instance, **kwargs):
#         instance.profile.save()


class BookMark(models.Model):
    """주차장 즐겨찾기"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
