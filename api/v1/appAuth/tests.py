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

    def test_user_signup(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.post(reverse('signup'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Тест запроса с неполными данными
        response = self.client.post(reverse('signup'), {'username': 'john', 'password': 'smith'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Тест запроса с полными данными
        response = self.client.post(
            reverse('signup'),
            {'username': 'userr', 'password': 'qwert', 'email': 'efrr@rtttt.rr'}
        )
        self.assertContains(response, 'auth_token', status_code=201)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
