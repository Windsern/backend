from django.contrib import admin
from .models import Users, Building, Checking, CheckingsBuildings

# Register your models here.
# from .models import Book

# admin.site.register(Book)

admin.site.register(Users)
admin.site.register(Building)
admin.site.register(Checking)
admin.site.register(CheckingsBuildings)