from django.db import models

class Student(models.Model):
    TEAM=[
        ('B','Blue Team'),
        ('O','Orange Team'),
        ('G','Green Team')
        ]
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100)
    team=models.CharField(max_length=1,choices=TEAM,default="B")

    def __str__(self):
        return self.name

class Rp(models.Model):
    room_no=models.IntegerField(primary_key=True)
    student=models.OneToOneField(Student,on_delete=models.CASCADE,related_name="rp")

    def __str__(self):
        return self.room_no