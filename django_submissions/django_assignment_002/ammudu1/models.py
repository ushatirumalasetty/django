from django.db import models

class User(models.Model):
    name=models.CharField(max_length=100)
    age=models.CharField(max_length=100)
    place=models.CharField(max_length=100)

class Netflix_account(models.Model):
    account_id=models.IntegerField(primary_key=True)
    account_name=models.CharField(max_length=100)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="netflix_account")
    

    
    