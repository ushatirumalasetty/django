from django.contrib import admin
from .models import *

admin.site.register(Actor)
admin.site.register(Rating)
admin.site.register(Movie)
admin.site.register(Director)
admin.site.register(Cast)