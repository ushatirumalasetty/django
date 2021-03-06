from django.db import models


class Actor(models.Model):
    GENDER=(
        ("FEMALE","female"),
        ("MALE","male"),
        )
    actor_id=models.CharField(max_length=100,primary_key=True)
    name=models.CharField(max_length=100 )
    gender=models.CharField(max_length=10,choices=GENDER)

class Director(models.Model):
    name=models.CharField(max_length=100,unique=True)

class Movie(models.Model):
    name=models.CharField(max_length=100)
    movie_id=models.CharField(max_length=100,primary_key=True)
    release_date=models.DateField()
    box_office_collection_in_crores=models.FloatField()
    director=models.ForeignKey(Director,on_delete=models.CASCADE,related_name="dir")
    actors=models.ManyToManyField(Actor,through='Cast',related_name="movies")

class Cast(models.Model):
    actor=models.ForeignKey(Actor,on_delete=models.CASCADE,related_name="act")
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="move")
    role=models.CharField(max_length=50)
    is_debut_movie=models.BooleanField(default=False)


class Rating(models.Model):
    movie=models.OneToOneField(Movie,on_delete=models.CASCADE,default=None,related_name="mov")
    rating_one_count=models.IntegerField(default=0)
    rating_two_count=models.IntegerField(default=0)
    rating_three_count=models.IntegerField(default=0)
    rating_four_count=models.IntegerField(default=0)
    rating_five_count=models.IntegerField(default=0)