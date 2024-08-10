from django.test import TestCase , Client
from django.urls import reverse
from product.views import *
from rest_framework.authtoken.models import Token

class TestViews(TestCase):
    def setUp(self):
        self.productsurl = reverse('main')
        self.searchurl = reverse('search')
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.reviewurl = reverse('reviews',args=[1])
        self.token = Token.objects.create(user=self.user)
    def test_product_get(self):
        response = self.client.get(self.productsurl,headers= {'Authorization':'token '+self.token.key})
        self.assertEquals(response.status_code,200)
    def test_search(self):
        response = self.client.get(self.searchurl,headers= {'Authorization':'token '+self.token.key})
        self.assertEquals(response.status_code,200)
    def test_product_post(self):
        response = self.client.post(self.productsurl,{'title':'TV LG','description':'description of tv','price':1200,'brand':'LG','category':'electronics','seller':self.user},headers= {'Authorization':'token '+self.token.key})
        self.assertEquals(response.status_code,201)
    def test_product_POST_no_data(self):
        response = self.client.post(self.productsurl,headers= {'Authorization':'token '+self.token.key})
        self.assertEquals(response.status_code, 403)
    def test_review_POST(self):
        product = Product.objects.create(
            title='TV LG',description='description of tv',price=1200,brand='LG',category='electronics',seller=self.user
        )
        response = self.client.post(self.reviewurl,{'product':product,'user':self.user,'rate':3,'comment':'my comment'},headers= {'Authorization':'token '+self.token.key})
        self.assertEquals(response.status_code,201)
    def test_review_delete(self):
        product = Product.objects.create(
            title='TV LG',description='description of tv',price=1200,brand='LG',category='electronics',seller=self.user
        )
        review = Review.objects.create(product=product,user=self.user,rate=3,comment='any comment')
        self.reviewurl = reverse('reviews',args=[product.pk])
        response = self.client.delete(self.reviewurl,headers= {'Authorization':'token '+self.token.key})
        self.assertEquals(response.status_code,204)
    def test_review_POST_no_data(self):
        response = self.client.post(self.reviewurl,headers= {'Authorization':'token '+self.token.key})
        self.assertEquals(response.status_code, 403)
        