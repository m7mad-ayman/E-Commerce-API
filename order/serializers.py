from rest_framework.serializers import ModelSerializer
from .models import * 

class CartSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["user","product","quantity"]

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"