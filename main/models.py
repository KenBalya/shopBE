from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Handle the age field for superuser
        extra_fields.setdefault('age', 18)  # Assuming 18 as a default age for superusers

        return self.create_user(username, email, password, **extra_fields)


class MyUser(AbstractUser):
    GENDER_CHOICES = [('MEN', 'Men'), ('WOMEN', 'Women'), ('NONBINARY', 'Nonbinary')]
    LANGUAGES_CHOICES = [('ENGLISH', 'English'), ('INDONESIA', 'Indonesia')]

    gender = models.CharField(choices=GENDER_CHOICES, max_length=255)
    age = models.PositiveSmallIntegerField(null=True, blank=True)  # Made age optional
    language = models.CharField(choices=LANGUAGES_CHOICES, max_length=255)
    objects = MyUserManager()

    def __str__(self):
        return self.username

