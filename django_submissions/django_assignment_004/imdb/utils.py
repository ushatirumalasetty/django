from .models import *
from django.db.models import *


def get_average_box_office_collections():
    if Movie.objects.all().count()==0:
        return 0
    m= Movie.objects.aggregate(a=Avg("box_office_collection_in_crores"))
    return round(m["a"],3)


def get_movies_with_distinct_actors_count():
    return Movie.objects.annotate(actors_count=Count("actors",distinct=True))

def get_male_and_female_actors_count_for_each_movie():
    m=(Count("actors",filter=Q(actors__gender="MALE"),distinct=True))
    f=(Count("actors",filter=Q(actors__gender="FEMALE"),distinct=True))
    return Movie.objects.annotate(male_actors_count=m,female_actors_count=f)




def get_roles_count_for_each_movie():
    return Movie.objects.annotate(roles_count=Count("move__role",distinct=True))




def get_role_frequency():
    dic={}
    p=Cast.objects.values_list("role").annotate(Count("actor",distinct=True))
    for i in p:
        dic[i[0]]=i[1]
    return dic


def get_role_frequency_in_order():

    return list(Cast.objects.values_list("role").annotate(Count("actor")).order_by("-movie__release_date"))




def get_no_of_movies_and_distinct_roles_for_each_actor():
    if  Actor.objects.all().count():
         return Actor.objects.annotate(movies_count=Count("movies",distinct=True),roles_count=Count("act__role",distinct=True))
    else:
         return [] 

def get_movies_with_atleast_forty_actors():
    if Movie.objects.all().count()==0:
        return 0
    return Movie.objects.annotate(actors_count=Count("actors",distinct=True)).filter(actors_count__gte=40)


def get_average_no_of_actors_for_all_movies():

    if Movie.objects.all().count()==0:
        return 0
    else:
        m=Movie.objects.annotate(t=Count('actors',distinct=True)).aggregate(a=Avg("t"))
        return round(m["a"],3)
