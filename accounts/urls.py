from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name="login"),
    path('<int:user_pk>/edit/', views.edit, name='edit'),
    path('select/', views.select, name='select'),
    # path('<int:movie_pk>/select_score/', views.select_score, name="select_score"),
    path('get_list/<int:idx>/', views.get_list, name='get_list'),
    path('logout/', views.logout, name='logout'),
    path('signout/', views.user_delete, name='signout'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
]
