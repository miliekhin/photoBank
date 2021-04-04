from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class AuthTests(APITestCase):

    def setUp(self):
        self.userr = User.objects.create_user(username='testuser', password="qwerty")
        self.userr.save()

    def test_logout_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.userr.auth_token))
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
