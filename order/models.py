from django.db import models
from django.contrib.auth.models import User
from product.models import Product
import uuid

# Create your models here.

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    city = models.CharField(max_length=100,blank=False,null=False)
    zipcode = models.CharField(max_length=100,blank=False,null=False)
    country = models.CharField(max_length=100,blank=False,null=False)
    street = models.CharField(max_length=100,blank=False,null=False)
    phone_num = models.CharField(max_length=100,blank=False,null=False)
    payway = models.CharField(max_length=100,blank=False,null=True,choices=[('cod','cod'),("card","card")],default="cod")
    paystatue = models.CharField(max_length=100,blank=False,null=True,choices=[('paid','paid'),("not paid","not paid")],default="not paid")
    user = models.ForeignKey(User,blank=False,on_delete=models.CASCADE)
    statue = models.CharField(max_length=100,blank=False,null=False,choices=[
        ('processing','processing'),("shipped","shipped"),("delivered","delivered")],default="processing")
    order_code = models.CharField(max_length=10,unique=True,blank=False,null = False) 
    orderedat = models.DateTimeField (auto_now=True)
    total_price = models.DecimalField(max_digits=10,decimal_places=2,blank=False)
    def __str__(self):
        return "{0} , {1}".format(self.user,self.order_code)

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User,blank=False,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,blank=False,on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(blank = False,null=False)
    order_id = models.CharField(max_length=10,blank=True,null= True)