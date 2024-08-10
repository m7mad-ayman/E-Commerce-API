from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status
from .models import *
from .serializer import *
from django.core.paginator import Paginator
@api_view(['GET','POST'])
def productview(request):
    if request.method == "GET":
        paging = Paginator(Product.objects.all(),2)
        try:
            product = paging.get_page(request.GET.get('page'))
        except:
            product = paging.get_page(request.GET.get(1))

        serial = ProductSerializer(product,many=True)
        return Response(serial.data)
    elif request.method == "POST":
        if request.data == {}:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            product = Product.objects.create(
            title = request.data['title'],
            description = request.data['description'],
            price = request.data['price'],
            brand = request.data['brand'],
            category = request.data['category'],
            seller = request.user
        )
            product.save()
            return Response(status=status.HTTP_201_CREATED)

@api_view(["GET"])
def search(request):
    try :
        
        product = Product.objects.filter(category__exact= request.data['category'])
        
        if ProductSerializer(product,many=True).data != []:
            return Response(ProductSerializer(product,many=True).data)
        else :
            return 1/0
    except:
          try :
        
             product = Product.objects.filter(title__contains= request.data['search'])
             if ProductSerializer(product,many=True).data != []:
                 return Response(ProductSerializer(product,many=True).data)
             else :
                return 1/0
          except:
                try:
         
                   product = Product.objects.filter(brand__exact= request.data['brand'] )
                   if ProductSerializer(product,many=True).data != []:
                      return Response(ProductSerializer(product,many=True).data)
                   else :
                     return 1/0
                except:
                   return Response({'message':'NOT FOUND'})

@api_view(["POST","PUT","DELETE"])
def re_view(request,pk):
    if request.method == "POST":
        if request.data == {}:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            if not Review.objects.filter(product=Product.objects.get(id=pk),user=request.user).exists():
                try:
                    product =Product.objects.get(id=pk)
                    review = Review()
                    review.product = product
                    review.user = request.user
                    try:
                        review.comment = request.data["comment"]
                    except:
                        pass
                    review.rate = request.data['rate']
                    review.save()
                    ratings = Review.objects.filter(product=Product.objects.get(id=pk))
                    serial =ReviewSerializer(ratings,many=True)
                    if len(serial.data) >0:
                        sum=0
                        for rating in serial.data:
                            sum+=rating["rate"]
                        avg = sum/len(serial.data)
                        product.rating = avg
                        product.save()
                    else:
                        product.rating = 0
                        product.save()
                    return Response({"process":"Review Accepted"},status=status.HTTP_201_CREATED)
                except Exception as error:
                    return Response({"error":str(error)})
            else:
                return Response({"Message":"Review already exist"})
    elif request.method == "PUT":
            try:
                product =Product.objects.get(id=pk)
                review = Review.objects.get(product = product,user=request.user)
                try:
                    review.comment = request.data["comment"]
                except:
                    pass
                review.rate = request.data['rate']
                review.save()
                ratings = Review.objects.filter(product=Product.objects.get(id=pk))
                serial =ReviewSerializer(ratings,many=True)
                if len(serial.data) >0:
                    sum=0
                    for rating in serial.data:
                        sum+=rating["rate"]
                    avg = sum/len(serial.data)
                    product.rating = avg
                    product.save()
                else:
                    product.rating = 0
                    product.save()
                return Response({"process":"Review Updated"})
            except Exception as error:
                return Response({"error":str(error)})
    elif request.method == "DELETE":
        try:
                product =Product.objects.get(id=pk)
                review = Review.objects.get(product = product,user=request.user)
                review.delete()
                ratings = Review.objects.filter(product=Product.objects.get(id=pk))
                serial =ReviewSerializer(ratings,many=True)
                if len(serial.data) >0:
                    sum=0
                    for rating in serial.data:
                        sum+=rating["rate"]
                    avg = sum/len(serial.data)
                    product.rating = avg
                    product.save()
                else:
                    product.rating = 0
                    product.save()
                return Response({"Message":"Review Deleted"},status=status.HTTP_204_NO_CONTENT)

        except Exception as error:
                return Response({"error":str(error)})
    

