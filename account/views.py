from django.shortcuts import render
from .serializer import RegisterSerializer
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
import datetime
from .models import *
from .tasks import sending_mail
@api_view(["POST"])
@permission_classes([AllowAny])
def registerview(request):
    if request.method == "POST":
        try:
            serial = RegisterSerializer(data=request.data)
            if serial.is_valid():
                if not User.objects.filter(username = request.data['email']).exists():
                    user=User()
                    user.username = request.data["email"]
                    user.first_name = request.data["first_name"]
                    user.last_name = request.data["last_name"]
                    if request.data['password'] == request.data['confirm']:
                        user.password = make_password(request.data["password"])
                        user.save()
                        token=Token.objects.get_or_create(user=user)

                        return Response({"email":user.username,"token":str(token[0])}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"message":"password did't match"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    
                else:
                    return Response({"message":"Email already exist"}, status=status.HTTP_403_FORBIDDEN)
            else :
                return Response(serial.errors, status=status.HTTP_403_FORBIDDEN)
        except Exception as error:
            return Response({"error":str(error)}, status=status.HTTP_403_FORBIDDEN)

@api_view(["POST"]) 
@permission_classes([AllowAny])
def resetview(request):
    if request.method == "POST":
        try:
            email = request.data['email']
            code = get_random_string(length=5)
            expired = datetime.datetime.now()+datetime.timedelta(minutes=1)
            reset = Reset()
            user = User.objects.get(username=email)
            reset.profile = user
            reset.token = code
            reset.expire = expired
            reset.save()
            sending_mail.delay(request.data['email'],code)
            return Response("email is sent",status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({"error":str(error)},status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"]) 
@permission_classes([AllowAny])
def changeview(request,tok):
    try:
        if Reset.objects.get(token=tok).expire.replace(tzinfo=None) >datetime.datetime.now():
            if request.data['password'] == request.data['confirm']:
                user = Reset.objects.get(token=tok).profile
                user.password=request.data['password']
                user.save()
                Reset.objects.get(token=tok).delete()
                return Response({"message":"password changed"},status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"message":"password did't match"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            Reset.objects.get(token=tok).delete()
            return Response({"message":"token is not valid"},status=status.HTTP_408_REQUEST_TIMEOUT)
    except Exception as error:
        return Response({"error":str(error)},status=status.HTTP_403_FORBIDDEN)






        

    