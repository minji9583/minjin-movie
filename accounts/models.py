from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from movies.models import Movie
# Create your models here.

class User(AbstractUser):
    bgc = models.TextField()
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings',)
