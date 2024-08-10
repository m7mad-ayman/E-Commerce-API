from django.urls import path 
from .views import *

urlpatterns = [
    path('cart/',cartview),
    path('order/',revieworderview),
    path('order/<str:code>',orderview),
    ]