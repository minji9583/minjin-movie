from django.contrib import admin
from .models import Genre, Actor, Movie
# Register your models here.
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    
class ActorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'audience', 'open_date', 'director', 'description']
    
admin.site.register(Genre, GenreAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Movie, MovieAdmin)