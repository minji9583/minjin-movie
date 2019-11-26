from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.TextField()
    
class Actor(models.Model):
    name = models.TextField()
    image_url = models.TextField(blank=True)
    

class Movie(models.Model):
    title = models.TextField()
    audience = models.IntegerField()
    poster_url = models.TextField()
    open_date = models.TextField()
    director = models.TextField()
    description = models.TextField()
    video_key = models.TextField(blank=True)
    actors = models.ManyToManyField(Actor, related_name="filmo")
    genres = models.ManyToManyField(Genre, related_name="included")
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_movies")
    hate_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="hate_movies")   
    score_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through = 'Score', related_name = 'score_movies')
    
# Score가 중개모델
class Score(models.Model):
    score = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    

class Comment(models.Model):
    content = models.CharField(max_length=140)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
 
# bash
# python csv2json.py movies.csv movies.Movie