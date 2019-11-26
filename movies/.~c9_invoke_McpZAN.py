import requests, csv, pprint, datetime
import math, random
from bs4 import BeautifulSoup as bs
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Genre, Actor, Comment, Score
from django.contrib import messages
from django.http import JsonResponse
from .forms import CommentForm, ScoreForm
from django.contrib.auth import get_user_model

client_id = '6nendm3Boyb4WkJDKnYt'
client_secret = 'hWhoO2eATg'
headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }


@login_required
# Create your views here.
def index(request):
    return

@login_required
def list(request):
    users = get_user_model()
    movies = Movie.objects.all()
    genres = Genre.objects.all()
    me = request.user
    score_movies = me.score_movies.all()
    if len(score_movies) == 0:
        return render(request, 'accounts/select.html')
    else:
        genre_count = [0]*(len(genres)+1)
        for score_movie in score_movies:
            sgs = score_movie.genres.all()
            for sg in sgs:
                genre_count[sg.pk] += 1
        genre_max_value = max(genre_count)
        genre_max_value_count = genre_count.count(genre_max_value)
        genre_reco_movies = []
        if genre_max_value_count > 1:
            for i in range(2):
                index = genre_count.index(genre_max_value)
                genre_count[index] = 0
                genre = get_object_or_404(Genre, pk=index)
                genre_movie = genre.included.all()
                for i in range(4):
                    genre_reco_movies.append(random.choice(genre_movie))
        else:
            index = genre_count.index(genre_max_value)
            genre = get_object_or_404(Genre, pk=index)
            genre_movie = genre.included.all()
            for i in range(6):
                random_movie_g = random.choice(genre_movie)
                if random_movie_g not in genre_reco_movies:
                    genre_reco_movies.append(random_movie_g)
                
        actors = Actor.objects.all()
        actor_count = [0]*(len(actors)+1)
        for score_movie in score_movies:
            score_actorset = score_movie.genres.all()
            for score_actor in score_actorset:
                actor_count[sg.pk] += 1
        actor_max_value = max(actor_count)
        actor_max_value_count = actor_count.count(actor_max_value)
        actor_reco_movies = []
        if actor_max_value_count > 1:
            for i in range(2):
                index = actor_count.index(actor_max_value)
                actor_count[index] = 0
                actor = get_object_or_404(Actor, pk=index)
                actor_movie = actor.included.all()
                for i in range(4):
                    random_movie_a = random.choice(actor_movie)
                    if random_movie_a not in actor_reco_movies:
                        actor_reco_movies.append(random_movie_a)
                        
        else:
            index = actor_count.index(actor_max_value)
            actor = get_object_or_404(Actor, pk=index)
            actor_movie = actor.filmo.all()
            for i in range(6):
                random_movie_a = random.choice(actor_movie)
                if random_movie_a not in actor_reco_movies:
                    actor_reco_movies.append(random_movie_a)

    #
    # def sim_pearson(users, name1, name2):
    #     sumX, sumY, sumPowX, sumPowY, sumXY, count = 0, 0, 0, 0, 0, 0
    #     person1 = users.objects.get(pk=name1)
    #     person2 = users.objects.get(pk=name2)
    #     for movie in person1.score_movies.all():
    #         if movie in person2.score_movies.all():
    #             sumX += movie.score_set.get(user=person1).score
    #             sumY += movie.score_set.get(user=person2).score
    #             sumPowX += pow(movie.score_set.get(user=person1).score, 2)
    #             sumPowY += pow(movie.score_set.get(user=person2).score, 2)
    #             sumXY += movie.score_set.get(user=person1).score * movie.score_set.get(user=person2).score
    #             count += 1
        # return (sumXY - ((sumX*sumY)/count))/ math.sqrt( (sumPowX - (pow(sumX,2) / count)) * (sumPowY - (pow(sumY,2)/count)))

    
    # # index는 몇 위까지 출력
    # def top_match(users, name, index=3, sim_function=sim_pearson):
    #     li = []
    #     me = users.objects.get(pk=name)
    #     for i in users.objects.all():
    #         if me.username != i.username:
    #             li.append((sim_function(users, name, i.pk), i.pk)) # i는 다른 사용자
    #     li.sort()
    #     li.reverse()
    
    #     return li[:index]# 
    
    # movies = Movie.objects.all()
    # def getRecommendation(movies, person, sim_function=sim_pearson):
    #     result = top_match(users, person, 1)
    #     simSum, score = 0, 0 # 유사도 합을 위한 변수, 평점 합을 위한 변수
    #     li = [] # 리턴을 위한 리스트
    #     score_dic = {} # 유사도 총합을 위한 dic
    #     sim_dic = {} # 평점 총합을 위한 dic
        
    #     for sim, name in result:
    #         if sim < 0: continue #유사도가 양수인 사람만
    #         for movie in users.objects.get(pk=name).score_movies.all():
    #             if movie not in users.objects.get(pk=person).score_movies.all():
    #                 score += sim * movie.score_set.get(user_id=name).score # 그사람의 영화 평점 * 유사도
    #                 score_dic.setdefault(movie.pk, 0) # 기본값 설정
    #                 score_dic[movie.pk] += score
    #                 sim_dic.setdefault(movie.pk, 0)
    #                 sim_dic[movie.pk] += sim
    #             score = 0
    #     for key in score_dic:
    #         score_dic[key]=score_dic[key]/sim_dic[key] # 평점 총합/ 유사도 총합
    #         # li.append((score_dic[key],key)) # list((tuple))의 리턴을 위해서.
    #         li.append(key)
    #     li.sort()
    #     li.reverse()
    #     return li
    # movie_list = getRecommendation(movies, request.user.pk)
    # result_list = []
    # for movie in movie_list:
    #     result_list.append(Movie.objects.get(pk=movie))
    # context = {'movies': movies, 'result_list': result_list, 'genre_reco_movies':genre_reco_movies}
    # # context = {'movies': movies}
    context = {'movies': movies, 'genre_reco_movies':genre_reco_movies, 'actor_reco_movies':actor_reco_movies, 'genres':genres}
    return render(request, 'movies/list.html', context)

@login_required
def boxoffice(request):
    genres = Genre.objects.all()
    key = '5c7fef1ea6cdb4c84fafc839095a8b2f'
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'
    date = datetime.datetime.now() - datetime.timedelta(weeks=1)
    target = date.strftime('%Y%m%d')
    address = "{0}?key={1}&targetDt={2}&weekGb=0".format(url, key, target)
    response = requests.get(address).json()
    during = response['boxOfficeResult']['showRange']
    movie_list = []
    # pprint.pprint(response)
    # pprint.pprint(response['boxOfficeResult']['weeklyBoxOfficeList'])
    # for movie in response['boxOfficeResult']['weeklyBoxOfficeList']:
    #     pprint.pprint(movie)
    #     # print(Movie.objects.filter(title=movie['movieNm']))
    #     # print('------------------------------')
    #     tmp = Movie.objects.filter(title=movie['movieNm'])
    #     if tmp:
    #         movie_list.append(tmp[0])
    #     else:
    #         pass
    #         new_data = Movie()
    #         new_data.title = movie['movieNm']
    #         naver_url = 'https://openapi.naver.com/v1/search/movie.json?query={0}'.format(movie['movieNm'])
    #         naver_res = requests.get(naver_url, headers=headers).json()
    #         code = naver_res['items'][0]['link'][51:]
    #         img_add = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode={0}'.format(code)
    #         res = requests.get(img_add).text
    #         soup = bs(res, 'html.parser')
    #         new_data.poster_url = soup.select_one('#targetImage')
    #         new_data.audience = movie['audiCnt']
    #         new_data.open_data = movie['openDt']
    #         new_data.save()
    print(movie_list)
    # context = {'response': response, 'movie_list': movie_list, 'genres':genres}
    context = {'movie_list': movie_list}
    return render(request, 'movies/boxoffice.html', context)
    
    
@login_required
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    actors = movie.actors.all()
    genres = Genre.objects.all()
    comments = movie.comment_set.all()
    comment_form = CommentForm()
    scores = movie.score_set.all()
    like_user_count = movie.like_users.count()
    print(type(movie.video_key))
    context = {'movie': movie, 'actors': actors, 'genres': genres, 'comment_form':comment_form, 'comments':comments, 'scores':scores}
    return render(request, 'movies/detail.html', context)

@login_required    
def genre_detail(request, genre_pk):
    genre = get_object_or_404(Genre, pk=genre_pk)
    genres = Genre.objects.all()
    genre_movie =  genre.included.all()
    context = {'genre':genre, 'genres':genres, 'genre_movie':genre_movie}
    return render(request, 'movies/genre_detail.html', context)
 
@login_required   
def actor_detail(request, actor_pk):
    actor = get_object_or_404(Actor, pk=actor_pk)
    genres = Genre.objects.all()
    context = {"actor":actor, 'genres':genres}
    return render(request, 'movies/actor_detail.html', context)
    
@login_required
def search(request):
#     # 1. 내가 만든 모델들
#     # 2. variable routing(해당 x)
#     # 3. form(O)
    # name = request.GET.get('name')
    query = request.GET.get('query')
    # movies = Movie.objects.all()
    searchResult = Movie.objects.filter(title__contains=query)
    # 리턴값이 쿼리셋, 일치하면 첫번째것으로 바로 들어가게 first붙여줌
    # filter대신 get쓸 수 있음 그럼 first안써도 됨
    # if not movie:
    #     messages.warning(request, f'{name}을 찾을 수 없습니다.')
    #     return redirect('movies:list')
    # return redirect('movie:detail', movie.pk)
    context = {'searchResult': searchResult, 'query': query}
    return render(request, 'movies/search.html', context)


@login_required
def userpage(request, user_pk):
    User = get_user_model()
    target_user = get_object_or_404(User, pk=user_pk)
    genres = Genre.objects.all()
    comments = target_user.comment_set.all()
    like_movies = target_user.like_movies.all()
    hate_movies = target_user.hate_movies.all()
    score_movies = target_user.score_set.all()
    context = {
                'target_user':target_user, 
                'comments':comments, 'genres':genres, 
                'like_movies':like_movies, 
                'hate_movies':hate_movies,
                'score_movies':score_movies
                }
    return render(request, 'movies/userpage.html', context)
    
    
@login_required
def comment_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.movie = movie
        comment.user = request.user
        comment.save()
        data = {'username': comment.user.username, 
                'commentUserPk':comment.user.pk,
                'content': comment.content,
                'postPk': comment.movie.pk,
                'commentPk': comment.pk
                }
        return redirect('movies:detail', movie_pk)
        

@login_required
def comment_delete(request, movie_pk, comment_pk):
    # 댓글 삭제할 때 원래는 comment_pk만 있으면 되는데
    # redirect할 땐 post_pk가 필요하니까 같이 넘겨주기
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect('movies:detail', movie_pk)
    
@login_required
def score_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # print(score)
    movie_score = request.POST.get('movie_score')
    # print(score)
    user = request.user
    # print(user)
    # movie = movie_pk
    score_list = Score.objects.filter(movie=movie).filter(user=user)
    if score_list:
        # 수정
        my_score = score_list[0]
        my_score.score = request.POST.get('movie_score')
        my_score.save()
    else:
        score = Score()
        score.score = movie_score
        score.user = request.user
        score.movie = movie
        score.save()
    return redirect('movies:detail', movie_pk)

@login_required
def score_delete(request, movie_pk, score_pk):
    score = get_object_or_404(Score, pk=score_pk)
    score.delete()
    return redirect('movies:detail', movie_pk)

@login_required
def like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user
    if user in movie.like_users.all():
        movie.like_users.remove(user)
    else:
        movie.like_users.add(user)
    return redirect('movies:detail', movie_pk)

@login_required
def hate(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user
    if user in movie.hate_users.all():
        movie.hate_users.remove(user)
    else:
        movie.hate_users.add(user)
    return redirect('movies:detail', movie_pk)

def user_score_delete(request, movie_pk, score_pk):
    score = get_object_or_404(Score, pk=score_pk)
    score.delete()
    return redirect('movies:userpage', movie_pk)
    
def user_comment_delete(request, movie_pk, score_pk):
    score = get_object_or_404(Score, pk=score_pk)
    score.delete()
    return redirect('movies:userpage', movie_pk)