from django.urls import path 
from .views import *

urlpatterns = [
    path('register/',registerview,name='register'),
    #path('login/',loginview),
    path('reset/',resetview,name='reset'),
    path('change/<str:tok>',changeview,name='pasch'),
    ]