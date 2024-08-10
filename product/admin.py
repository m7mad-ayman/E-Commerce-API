from django.contrib import admin
from .models import *
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title','price','id']

admin.site.register(Product,TaskAdmin)

admin.site.register(Review)
