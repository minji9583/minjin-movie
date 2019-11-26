from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from .forms import UserCustomCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from movies.models import Movie, Score
from .serializers import MovieSerializer


def start(request):
    return render(request, 'accounts/start.html')
    
def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:list')
    if request.method == "POST":
        User = get_user_model()
        username = request.POST.get('username')
        password = request.POST.get('password')
        bgc = request.POST.get('bgc')
        user = User.objects.create_user(username, password)
        user.bgc = bgc
        user.save()
        auth_login(request, user)
        return redirect('accounts:select')
    else:
        return render(request, 'accounts/signup.html')
    
def edit(request, user_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_pk)
    if request.method == "POST":
        user.username = request.POST.get('username')
        user.password = user.POST.get('password')
        user.bgc = request.POST.get('bgc')
        user.save()
        auth_login(request, user)
        return redirect('movies:userpage', user_pk)
    else:
        context = {'user':user}
    return render(request, 'accounts/edit.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('movies:list')
    if request.method == "POST":
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect(request.GET.get('next') or 'movies:list')
    else:
        login_form = AuthenticationForm()
    context = {'login_form':login_form}
    return render(request, 'accounts/login.html', context)
    
@login_required
def logout(request):
    auth_logout(request)
    messages.info(request, '안전하게 로그아웃되었습니다')
    return redirect('movies:list')
    
@login_required
def user_delete(request):
    request.user.delete()
    messages.success(request, '탈퇴되었습니다.')
    return redirect('movies:list')
    
def select(request):
    return render(request, 'accounts/select.html')
    
# def select_score(request, movie_pk):
#     movie = get_object_or_404(Movie, pk=movie_pk)
#     # # print(score)
#     movie_score = request.POST.get('movie_score')
#     # print(score)
#     user = request.user
#     # print(user)
#     # movie = movie_pk
#     score_list = Score.objects.filter(movie=movie).filter(user=user)
#     if score_list:
#         # 수정
#         my_score = score_list[0]
#         my_score.score = request.POST.get('movie_score')
#         my_score.save()
#     else:
#         score = Score()
#         score.score = movie_score
#         score.user = request.user
#         score.movie = movie
#         score.save()
#     return render(request, 'accounts/select.html')
    
    
@api_view(['GET'])
def get_list(request, idx):
    all_movies = Movie.objects.all()
    paginator = Paginator(all_movies, idx)
    contacts = paginator.get_page(1).object_list
    serializer = MovieSerializer(contacts, many=True)
    # content = JSONRenderer().render(serializer.data)
    # print(content)
    return Response(serializer.data)
    # return Response(serializers.serialize('json', contacts), safe=False)



@login_required
def follow(request, user_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_pk)
    if request.user in user.followers.all():
        user.followers.remove(request.user)
    else:
        user.followers.add(request.user)
    return redirect('movies:userpage', user_pk)