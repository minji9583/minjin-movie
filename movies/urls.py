from django.urls import path
from . import views

app_name = "movies"
urlpatterns = [
    # path('', views.index, name='index'),
    path('list', views.list, name='list'),
    path('boxoffice/', views.boxoffice, name='boxoffice'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('genres/<int:genre_pk>/', views.genre_detail, name="genre_detail"),
    path('actors/<int:actor_pk>/', views.actor_detail, name="actor_detail"),
    path('search/', views.search, name='search'),
    path('<int:movie_pk>/comment/', views.comment_create, name='create_comment'),
    path('<int:movie_pk>/comment/<int:comment_pk>/', views.comment_delete, name='comment_delete'),
    path('<int:movie_pk>/comment/<int:comment_pk>/user', views.user_comment_delete, name='user_comment_delete'),
    path('<int:movie_pk>/score/', views.score_create, name='score_create'),
    path('<int:movie_pk>/score/<int:score_pk>/', views.score_delete, name='score_delete'),
    path('<int:movie_pk>/score/<int:score_pk>/user', views.user_score_delete, name='user_score_delete'),
    path('userpage/<int:user_pk>', views.userpage, name="userpage"),
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('<int:movie_pk>/hate/', views.hate, name='hate')
]
