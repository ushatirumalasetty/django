from .models import *
from django.db import connection
from django.db.models import *
from django.core.exceptions import *
from collections import *



def get_average_rating_of_movie(movie_obj):
    try:
        movie_obj.rating
    except ObjectDoesNotExist:
        return 0
    rating_1=movie_obj.rating.rating_one_count
    rating_2=movie_obj.rating.rating_two_count
    rating_3=movie_obj.rating.rating_three_count
    rating_4=movie_obj.rating.rating_four_count
    rating_5=movie_obj.rating.rating_five_count
    sum=(rating_1*1+rating_2*2+rating_3*3+rating_4*4+rating_5*5)
    try:
        z=sum/(rating_5+rating_1+rating_2+rating_3+rating_4)
    except ZeroDivisionError:
        return 0

    return z


def total_rating_of_movie(movie_obj):
    try:
        movie_obj.rating
    except ObjectDoesNotExist:
        return 0
    rating_1=movie_obj.rating.rating_one_count
    rating_2=movie_obj.rating.rating_two_count
    rating_3=movie_obj.rating.rating_three_count
    rating_4=movie_obj.rating.rating_four_count
    rating_5=movie_obj.rating.rating_five_count
    z=(rating_5+rating_1+rating_2+rating_3+rating_4)

    return z






def  populate_database(actors_list, movies_list, directors_list, movie_rating_list):
    actor_opt_list=[]
    director_opt_list=[]
    cast_opt_list=[]
    rating_opt_list=[]
    movie_opt_list=[]
    for actors in actors_list:
       actor_obj=Actor(
           actor_id=actors["actor_id"],
           name=actors["name"],
           gender=actors["gender"]
       )
       actor_opt_list.append(actor_obj)
    Actor.objects.bulk_create(actor_opt_list)
    for directors in directors_list:
        director_obj=Director(
            name=directors
        )

        director_opt_list.append(director_obj)
    Director.objects.bulk_create(director_opt_list)
    d=Director.objects.all()
    for movies in movies_list:
        for i in d:
            if i.name==movies["director_name"]:
                p=i
                break

        movie_obj=Movie(
            movie_id=movies["movie_id"],
            name=movies["name"],
            box_office_collection_in_crores=movies["box_office_collection_in_crores"],
            release_date=movies["release_date"],
            director=p
        )
        movie_opt_list.append(movie_obj)

        for act in movies["actors"]:
            cast_obj=Cast(
                movie_id=movies["movie_id"],
                actor_id=act["actor_id"],
                role=act["role"],
                is_debut_movie=act["is_debut_movie"]
            )
            cast_opt_list.append(cast_obj)
    Movie.objects.bulk_create(movie_opt_list)
    Cast.objects.bulk_create(cast_opt_list)


    for ratings in movie_rating_list:
        rating_obj=Rating(
            movie_id= ratings["movie_id"],
            rating_one_count= ratings["rating_one_count"],
            rating_two_count= ratings["rating_two_count"],
            rating_three_count= ratings["rating_three_count"],
            rating_four_count= ratings["rating_four_count"],
            rating_five_count= ratings["rating_five_count"]
        )
        rating_opt_list.append(rating_obj)


    Rating.objects.bulk_create(rating_opt_list)

#task 2
def remove_all_actors_from_given_movie(movie_object):
    movie_object.actors.clear()

#task 3
def get_all_rating_objects_for_given_movies(movie_objs):
    return Rating.objects.filter(movie__in=movie_objs)


#task
def  get_movies_by_given_movie_names(movie_names,male=False):
    cast_details=Cast.objects.select_related('actor','movie__director','movie__rating').filter(movie__name__in=movie_names)
    movie_dic={}
    actor_dic={}
    cast_dic={}
    cast_lis=[]

    movie_details=defaultdict(list)
    lis=[]
    movies=[]
    cast_objs=[]

    for cast_obj in cast_details:
          movie_details[cast_obj.movie].append(cast_obj)

    for movies,clist in movie_details.items():
               movie_dic={"movie_id":0,"name":'',"cast":[],"box_office_collection_in_crores":"","release_date":"","director_name":"","average_rating":0,"total_number_of_ratings":0}
               movie_dic["movie_id"]=movies.movie_id
               movie_dic["name"]=movies.name
               movie_dic["box_office_collection_in_crores"]=movies.box_office_collection_in_crores
               movie_dic["release_date"]=str(movies.release_date)
               movie_dic["director_name"]=movies.director.name
               a=get_average_rating_of_movie(movies)
               movie_dic["average_rating"]=a
               t=total_rating_of_movie(movies)
               movie_dic["total_number_of_ratings"]=t
               for cast in clist:
                   actor_dic={}
                   cast_dic={}
                   if male==True and cast.actor.gender=="MALE":
                       continue
                   actor_dic["name"]=cast.actor.name
                   actor_dic["actor_id"]=cast.actor_id
                   cast_dic["actor"]=actor_dic
                   cast_dic["role"]=cast.role
                   cast_dic["is_debut_movie"]=cast.is_debut_movie
                   movie_dic["cast"].append(cast_dic)
               lis.append(movie_dic)
    return lis




#task 5
def get_all_actor_objects_acted_in_given_movies(movie_objs):
    return Actor.objects.filter(movie__in=movie_objs).distinct()







#task 6

def get_female_cast_details_from_movies_having_more_than_five_female_cast():

    female_cast_details=Movie.objects.filter(actors__gender="FEMALE").annotate(no_of_actors=Count("actors")).filter(no_of_actors__gt=5).values_list("name",flat=True)
    lists=get_movies_by_given_movie_names(female_cast_details,male=True)
    return lists






#task 7
def get_actor_movies_released_in_year_greater_than_or_equal_to_2000():
    cast_details=Cast.objects.select_related('actor','movie__director','movie__rating').filter(movie__release_date__year__gte=2000)
    movie_dic={}
    actor_dic={}
    cast_dic={}
    cast_lis=[]
    actor_details=defaultdict(list)

    lis=[]
    movies=[]
    cast_objs=[]

    for actor_obj in cast_details:
          actor_details[actor_obj.actor].append(actor_obj)

    for actors,movie_obj in actor_details.items():
        movies_in_2000={"name":"","actor_id":""}
        movies_in_2000["name"]=actors.name
        movies_in_2000["actor_id"]=actors.actor_id
        movie_details=defaultdict(list)
        for cast_obj in movie_obj:
               movie_details[cast_obj.movie].append(cast_obj)
        movies_by_given_movie_names=[]
        for movies,clist in movie_details.items():
               movie_dic={"movie_id":0,"name":'',"cast":[],"box_office_collection_in_crores":"","release_date":"","director_name":"","average_rating":0,"total_number_of_ratings":0}
               movie_dic["movie_id"]=movies.movie_id
               movie_dic["name"]=movies.name
               movie_dic["box_office_collection_in_crores"]=movies.box_office_collection_in_crores
               movie_dic["release_date"]=str(movies.release_date)
               movie_dic["director_name"]=movies.director.name
               a=get_average_rating_of_movie(movies)
               movie_dic["average_rating"]=a
               t=total_rating_of_movie(movies)
               movie_dic["total_number_of_ratings"]=t
               for cast in clist:
                   cast_dic={}
                   cast_dic["role"]=cast.role
                   cast_dic["is_debut_movie"]=cast.is_debut_movie
                   movie_dic["cast"].append(cast_dic)
                   movies_by_given_movie_names.append(movie_dic)
               movies_in_2000["movies"]=movies_by_given_movie_names
        lis.append(movies_in_2000)
    return lis



#task 8
def reset_ratings_for_movies_in_given_year(year):
    Rating.objects.filter(movie__release_date__year=year).update(rating_one_count=0,rating_two_count=0,rating_three_count=0,rating_four_count=0,rating_five_count=0)





