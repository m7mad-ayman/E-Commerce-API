from typing import List
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
import uuid
# Create your models here.
class Product(models.Model):
    options=(
        ('technology','technology'),
        ('home','home'),
        ('fashion','fashion'),
        ('accessories','accessories'),
        ('electronics','electronics'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length = 200,blank=False,null=False)
    description =models.CharField(max_length=1000,blank=False,null=False)
    price = models.DecimalField(max_digits=8,decimal_places=2,blank=False)
    brand = models.CharField(max_length=100,blank=False)
    category = models.CharField(max_length=100,choices=options,blank=False)
    seller = models.ForeignKey(User,on_delete=models.CASCADE,blank=False)
    stock = models.IntegerField(default=1,blank=False)
    created = models.DateTimeField(auto_now_add = True)
    rating = models.DecimalField(max_digits=2,decimal_places=1,validators=[MaxValueValidator(5),MinValueValidator(0)],default=0)
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title



class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product,blank=False,on_delete=models.CASCADE)
    user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    rate = models.IntegerField(validators=[MaxValueValidator(5),MinValueValidator(0)])
    comment = models.CharField(max_length=200,blank=True,null=True)
    at = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return '{0},{1}'.format(self.user,self.product)
    class Meta:
        unique_together = (("user","product"))