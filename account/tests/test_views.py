from django.test import TestCase ,Client
from account.views import *
from django.urls import reverse
from django.contrib.auth.models import User
import time

class TestAccountViews(TestCase):
    def setUp(self):
        self.registerurl = reverse('register')
        self.reseturl = reverse('reset')
        self.client=Client()

    def test_register(self):
        response = self.client.post(self.registerurl,{'email':'test@gmail.com','first_name':'test1','last_name':'test2','password':'test1234','confirm':'test1234'})
        self.assertEquals(response.status_code,201)

    def test_register_matching(self):
        response = self.client.post(self.registerurl,{'email':'test@gmail.com','first_name':'test1','last_name':'test2','password':'test1234','confirm':'test123'})
        self.assertEquals(response.status_code,406)

    def test_reset(self):
        email='test@gmail.com'
        User.objects.create(username=email,first_name='test1',last_name='test2',password='test1234')
        response = self.client.post(self.reseturl,{'email':email})
        self.assertEquals(response.status_code,201)

    def test_change_pass(self):
        user=User.objects.create(username='test1@gmail.com',first_name='test1',last_name='test2',password='test1234')
        expired = datetime.datetime.now()+datetime.timedelta(minutes=1)
        self.passchangeurl = reverse('pasch',args=['1234'])
        reset=Reset(profile=user,token='1234',expire=expired).save()
        response = self.client.post(self.passchangeurl,{'password':'changed','confirm':'changed'})
        self.assertEquals(response.status_code,202)

    def test_token_timeout(self):
        user=User.objects.create(username='test1@gmail.com',first_name='test1',last_name='test2',password='test1234')
        expired = datetime.datetime.now()+datetime.timedelta(seconds=1)
        reset=Reset(profile=user,token='1234',expire=expired).save()
        time.sleep(1)
        self.passchangeurl = reverse('pasch',args=['1234'])
        response = self.client.post(self.passchangeurl,{'password':'changed','confirm':'changed'})
        self.assertEquals(response.status_code,408)

    def test_change_matching(self):
        user=User.objects.create(username='test1@gmail.com',first_name='test1',last_name='test2',password='test1234')
        expired = datetime.datetime.now()+datetime.timedelta(minutes=1)
        self.passchangeurl = reverse('pasch',args=['1234'])
        reset=Reset(profile=user,token='1234',expire=expired).save()
        response = self.client.post(self.passchangeurl,{'password':'changed','confirm':'another'})
        self.assertEquals(response.status_code,406)