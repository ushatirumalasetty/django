from .models import *
from django.core.exceptions import ObjectDoesNotExist

def  populate_database(actors_list, movies_list, directors_list, movie_rating_list):
    for actors in actors_list:
       actor_obj=Actor(
           actor_id=actors["actor_id"],
           name=actors["name"]
       )
       actor_obj.save()

    for directors in directors_list:
        director_obj=Director(
            name=directors
        )

        director_obj.save()



    for movies in movies_list:
        movie_obj=Movie(
            movie_id=movies["movie_id"],
            name=movies["name"],
            box_office_collection_in_crores=movies["box_office_collection_in_crores"],
            release_date=movies["release_date"],
            director=Director.objects.get(name=movies["director_name"])
        )
        movie_obj.save()
        for act in movies["actors"]:
            cast_obj=Cast(
                movie=movie_obj,
                actor=Actor.objects.get(actor_id=act["actor_id"]),
                role=act["role"],
                is_debut_movie=act["is_debut_movie"]
            )
            cast_obj.save()


    for ratings in movie_rating_list:
        rating_obj=Rating(
            movie= Movie.objects.get(movie_id=ratings["movie_id"]),
            rating_one_count= ratings["rating_one_count"],
            rating_two_count= ratings["rating_two_count"],
            rating_three_count= ratings["rating_three_count"],
            rating_four_count= ratings["rating_four_count"],
            rating_five_count= ratings["rating_five_count"]
        )
        rating_obj.save()

def get_no_of_distinct_movies_actor_acted(actor_id):
    return Movie.objects.filter(actors__actor_id=actor_id).distinct().count()

def get_movies_directed_by_director( director_obj):
    return  list(director_obj.dir.all())

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

def delete_movie_rating(movie_obj):
   movie_obj.mov.delete()

def get_all_actor_objects_acted_in_given_movies(movie_objs):
    return list(Actor.objects.filter(movies__in=movie_objs).distinct())


def update_director_for_given_movie(movie_obj, director_obj):
    movie_obj.director=director_obj
    movie_obj.save()

def get_distinct_movies_acted_by_actor_whose_name_contains_john():
    return list(Movie.objects.filter(actors__name__contains="john").distinct())

def remove_all_actors_from_given_movie(movie_obj):
    movie_obj.actors.clear()

def get_all_rating_objects_for_given_movies(movie_objs):
    return list(Rating.objects.filter(movie__in=movie_objs))

def get_all_distinct_actors_for_given_movie(movie_obj):
    return movie_obj.actors.all().distinct()