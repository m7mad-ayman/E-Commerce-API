from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

class RegisterSerializer (ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password']
        exta_kwargs = {
            'first_name':{'required':True,'allow_blank':False},
            'last_name':{'required':True,'allow_blank':False},
            'email':{'required':True,'allow_blank':False},
            'password':{'required':True,'allow_blank':False,'min_length':8},
            
          
            }