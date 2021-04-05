from django.test import TestCase
from django.urls import reverse
from rest_framework import status
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from django.conf import settings
from .tasks import send_emails_to_top_users
from django.contrib.auth.models import User
from .models import UserTopNotifyMessage, Photo
import mock
from django.core.files import File


class PhotoAppTestCase(TestCase):
    def setUp(self):
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'photo_for_testing.jpg'
        self.msg = UserTopNotifyMessage.objects.create(subject='Congrats!',
                                                       message='Your photo in site top 3!',
                                                       from_email='qweqww@werwer.rr')
        self.users = []
        viewed = 0
        for i in range(3):
            u = User.objects.create_user(username=f'testuser{i}', password=f'qwerty{i}', email=f'qwert{i}@sdfgert.rt')
            u.save()
            self.users.append(u)
            for j in range(2):
                Photo.objects.create(owner=u, name=f'NewPhoto{j}', viewed=viewed, file_name=file_mock.name)
                viewed += 1

    def test_send_top_emails_count(self):
        """
        Проверка количества отправленных писем топ юзерам.
        Должно быть отправлено 2 письма: 1 писмо одному юзеру,
        при условии что у трех юзеров будет по два фото с количеством
        просмотров на один больше чем у предыдущего фото.
        """
        sent_count = send_emails_to_top_users()
        self.assertEqual(2, sent_count)

    def test_slideshow_success(self):
        # Регистрация юзера
        response = self.client.post(
            reverse('signup'),
            {'username': 'john', 'password': 'smith', 'email': 'sdfgf@rytuity.rr'}
        )
        self.assertContains(response, 'auth_token', status_code=201)
        token = json.loads(response.content)['auth_token']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Загружаем картинку
        image = io.BytesIO()
        Image.new('RGB', (640, 480), color='red').save(image, 'JPEG')
        image_file = SimpleUploadedFile('test_pic_file.jpg', image.getvalue())
        req_data = {"name": "MyPhoto", "file_name": image_file}
        response = self.client.post(
            reverse('user_photo_list_create'),
            req_data,
            format='multipart',
            HTTP_AUTHORIZATION=f'Token {token}'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Поднимаем просмотр фото на 1
        response = self.client.get(reverse('photo_retrieve', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем что просмотр увеличился
        self.assertEqual(1, json.loads(response.content)['viewed'])

        # Создаем слайдшоу из топ фото сайта
        response = self.client.get(reverse('site_slideshow'))
        # Проверяем что слайдшоу доступно
        self.assertRedirects(response,
                             settings.VIDEO_SLIDESHOW_URL + settings.TOP_PHOTOS_SLIDESHOW_FILE_NAME_SITE)

        # Создаем слайдшоу из топ фото юзера
        response = self.client.get(reverse('user_slideshow', kwargs={'user_id': 1}))
        # Проверяем что слайдшоу доступно
        self.assertRedirects(response,
                             settings.VIDEO_SLIDESHOW_URL + settings.TOP_PHOTOS_SLIDESHOW_FILE_NAME_USER)
