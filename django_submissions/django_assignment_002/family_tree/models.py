from django.db import models

GENDER=[
    ('M','Male'),
    ('F','Female')
    ]

RELATION=[
    ('F','Father'),
    ('M','Mother'),
    ('S','Sibling')
    ]

class Person(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    gender=models.CharField(max_length=1,choices=GENDER)
    relation=models.CharField(max_length=1,choices=RELATION)
    person=models.ForeignKey('self',on_delete=models.CASCADE,null=True,related_name="relatonship")
