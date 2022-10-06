from django.test import TestCase
from django.test import Client
from django.urls import reverse
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_user(self):
        ##test code
        GET_response = self.client.get(reverse('students'))

        #assertions
        self.assertEqual(GET_response,200)