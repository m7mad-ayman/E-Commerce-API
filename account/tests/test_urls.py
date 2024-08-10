from django.test import TestCase
from account.views import *
from django.urls import reverse,resolve

class TestAccount(TestCase):
    def setUp(self):
        self.registerurl = reverse('register')
        self.reseturl = reverse('reset')
        self.passchangeurl = reverse('pasch',args=['some-str'])
    def test_register(self):
        self.assertEquals(resolve(self.registerurl).func,registerview)
    def test_reset(self):
        self.assertEquals(resolve(self.reseturl).func,resetview)
    def test_passchange(self):
        self.assertEquals(resolve(self.passchangeurl).func,changeview)