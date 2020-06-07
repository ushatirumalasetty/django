from .models import *
from django.db.models import *
from django.core.exceptions import ObjectDoesNotExist
import json



def get_average_rating_of_movie(movie_obj):
    try:
        movie_obj.mov
    except ObjectDoesNotExist:
        return 0
    rating_1=movie_obj.mov.rating_one_count
    rating_2=movie_obj.mov.rating_two_count
    rating_3=movie_obj.mov.rating_three_count
    rating_4=movie_obj.mov.rating_four_count
    rating_5=movie_obj.mov.rating_five_count
    sum=(rating_1*1+rating_2*2+rating_3*3+rating_4*4+rating_5*5)
    try:
        z=sum/(rating_5+rating_1+rating_2+rating_3+rating_4)
    except ZeroDivisionError:
        return 0

    return z


def total_rating_of_movie(movie_obj):
    try:
        movie_obj.mov
    except ObjectDoesNotExist:
        return 0
    rating_1=movie_obj.mov.rating_one_count
    rating_2=movie_obj.mov.rating_two_count
    rating_3=movie_obj.mov.rating_three_count
    rating_4=movie_obj.mov.rating_four_count
    rating_5=movie_obj.mov.rating_five_count
    z=(rating_5+rating_1+rating_2+rating_3+rating_4)

    return z





def get_movies_by_given_movie_names(movie_names):
    movie_dic={}
    actor_dic={}
    cast_dic={}
    cast_lis=[]
    lis=[]
    for movie_name in movie_names:
       if type(movie_name)==str:
           movie_objs=Movie.objects.filter(name=movie_name)
       else:
           movie_objs=[movie_name]
       for movie_obj in movie_objs:
           movie_dic["movie_id"]=movie_obj.movie_id
           movie_dic["name"]=movie_obj.name
           casts=Cast.objects.filter(movie=movie_obj)
           for cast in casts: 
               actor_dic={}
               cast_dic={}
               actor_dic["name"]=cast.actor.name
               actor_dic["actor_id"]=cast.actor.actor_id
               cast_dic["actor"]=actor_dic
               cast_dic["role"]=cast.role
               cast_dic["is_debut_movie"]=cast.is_debut_movie
               cast_lis.append(cast_dic)
           movie_dic["cast"]=cast_lis
           movie_dic["box_office_collection_in_crores"]=movie_obj.box_office_collection_in_crores
           movie_dic["release_date"]=str(movie_obj.release_date)
           movie_dic["director_name"]=movie_obj.director.name
           a=get_average_rating_of_movie(movie_obj)
           movie_dic["average_rating"]=a
           t=total_rating_of_movie(movie_obj)
           movie_dic["total_number_of_ratings"]=t
           lis.append(movie_dic)
           movie_dic={}
           cast_lis=[]

    return lis

def get_movies_released_in_summer_in_given_years():
    movie_objs=Movie.objects.filter(Q(release_date__year__in=[2006,2007,2008,2009])& Q(release_date__month__in=[5,6,7]))
    return get_movies_by_given_movie_names(movie_objs)

def get_movie_names_with_actor_name_ending_with_smith():
    return Movie.objects.filter(actors__name__iendswith="smith").values_list("name",flat=True).distinct()


def get_movie_names_with_ratings_in_given_range():
    return Movie.objects.filter(Q(mov__rating_five_count__gte=1000),Q(mov__rating_five_count__lte=3000)).values_list("name",flat=True).distinct()


def get_movie_names_with_ratings_above_given_minimum():
    return Movie.objects.filter(Q(release_date__year__gt=2000)&Q(Q(mov__rating_five_count__gte=500)|Q(mov__rating_four_count__gte=1000)|Q(mov__rating_three_count__gte=2000)|Q(mov__rating_two_count__gte=4000)|Q(mov__rating_one_count__gte=8000))).values_list("name",flat=True).distinct()


def get_movie_directors_in_given_year():
    return Movie.objects.filter(release_date__year=2000).values_list("director__name",flat=True).distinct()


def get_actor_names_debuted_in_21st_century():
    return Actor.objects.filter(Q(movies__release_date__year__gt=2000)&Q(movies__release_date__year__lte=2100)&Q(act__is_debut_movie=True)).values_list("name",flat="True").distinct()


def get_director_names_containing_big_as_well_as_movie_in_may():
    return Movie.objects.filter(Q(name__contains="big")&Q(release_date__month=5)).values_list("director__name",flat=True).distinct()


def get_director_names_containing_big_and_movie_in_may():
    return Movie.objects.filter(Q(name__contains="big")&Q(release_date__month=5)).values_list("director__name",flat=True).distinct()


def reset_ratings_for_movies_in_this_year():
    Rating.objects.filter(movie__release_date__year=2000).update(rating_one_count=0,rating_two_count=0,rating_three_count=0,rating_four_count=0,rating_five_count=0)


