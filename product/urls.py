from django.urls import path ,include
from .views import productview, re_view ,search

urlpatterns = [
    path('',productview,name='main'),
    path('search/',search,name='search'),
    path('<int:pk>/review/',re_view,name="reviews"),
    ]