from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Actor)
admin.site.register(Movie)
admin.site.register(Director)
admin.site.register(Cast)
admin.site.register(Rating)
