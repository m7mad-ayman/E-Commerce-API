from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.response import Response
from .serializers import *
from product.models import Product
from django.utils.crypto import get_random_string


@api_view(["POST","GET","DELETE"])
@permission_classes([IsAuthenticated])
def cartview(request):
    if request.method == "POST":
        try:
               item = CartItem()
               item.user = request.user
               item.product = Product.objects.get(id=request.data["product_id"])
               try:
                   item.quantity = request.data["quantity"]
               except:
                   item.quantity = 1
               item.save()
               serial = CartSerializer(item)
               return Response(serial.data)
        except Exception as error :
            return Response(str(error))
    elif request.method == "GET":
        try:
            items = CartItem.objects.filter(user=request.user)
            serial = CartSerializer(items,many=True)
            if serial.data != []:
                total = 0
                for item in items :
                    price = float(item.product.price)
                    total = total+price*int(item.quantity)
                data = serial.data
                data.append({"total price":total})
                return Response(data)
            else:
                return Response({"message":"Your cart is empty"})
        except Exception as error :
            return Response(str(error))
    elif request.method == "DELETE":
        try:
            product=Product.objects.get(id=request.data["product_id"])
            item = CartItem.objects.get(user=request.user,product=product)
            item.delete()
            return Response({"message":"[ {0} ] deleted from your cart".format(product.title)})
        except Exception as error :
            return Response(str(error))

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def revieworderview(request):
    try:
        if request.method == "POST":
        
            order = Order()
            order.city = request.data["city"]
            order.zipcode = request.data["zipcode"]
            order.country =request.data["country"]
            order.street = request.data["street"]
            order.phone_num = request.data["phone"]
            order.user = request.user
            order.paystatue = request.data["paystatue"]
            order.payway = request.data["payway"]
            order.statue = request.data["statue"]
            items = CartItem.objects.filter(user=request.user)
            serialitems = CartSerializer(items,many=True)
            ordernum = get_random_string(length=10)
            while True:
                if not Order.objects.filter(order_code=ordernum).exists() :
                    order.order_code = ordernum
                    break
                else:
                    ordernum = get_random_string(length=10)
                    continue
            if serialitems.data != []:
               total = 0
               for item in items :
                  item.order_id = order.order_code
                  item.save()
                  price = float(item.product.price)
                  total = total+price*int(item.quantity)
                  
            else:
                return Response({"message":"Your cart is empty"})
            order.total_price = total
            

            order.save()
            serial = OrderSerializer(order).data
            serial["items"]=serialitems.data
            serial["message"]="Your order is done"
            return Response(serial)
    except Exception as error :
        return Response(str(error))



@api_view(["GET","DELETE"])
@permission_classes([IsAuthenticated])
def orderview(request,code):
    if request.method == "GET":
        try:
            order = Order.objects.get(order_code=code)
            serial = OrderSerializer(order)
            items = CartItem.objects.filter(user=request.user,order_id=code)
            serialitems = CartSerializer(items,many=True)
            serial = OrderSerializer(order).data
            serial["items"]=serialitems.data
            return Response(serial)
        except Exception as error :
            return Response(str(error))
    elif request.method == "DELETE":
        try:
            order = Order.objects.get(order_code=code)
            order.delete()
            return Response({"message":"Order {0} is deleted".format(str(code))})
        except Exception as error :
            return Response(str(error))