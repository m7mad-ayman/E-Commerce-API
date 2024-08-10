from django.test import TestCase
from django.urls import resolve ,reverse
from product.views import productview ,search ,re_view

class TestUrls(TestCase):
    def testproduct(self):
        url = reverse('main')
        self.assertEquals(resolve(url).func,productview)
    def testsearch(self):
        url = reverse('search')
        self.assertEquals(resolve(url).func,search)
    def testreview(self):
        url = reverse('reviews',args=[1])
        self.assertEquals(resolve(url).func,re_view)