from django.test import TestCase,Client
from django.urls  import reverse


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login(self):
        ##test code
        GET_response = self.client.get(reverse('login'))

        #assertions
        self.assertEqual(GET_response.status_code,200)

    def test_logout(self):
        response = self.client.get(reverse('logout'))
        #assert that the logout view is reachable
        self.assertEqual(response.status_code,200)
