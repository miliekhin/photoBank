import io
import os
from PIL import Image
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import mock
from django.core.files import File
from app.models import Photo
from api.v1.photos.serializers import PhotoSerializer
from django.conf import settings


class PhotosTests(APITestCase):
    TEST_IMAGE_NAME = 'test_image_07f479e0-fefb-4948-a4c7-f133cde7b7c2'
    TEST_IMAGE_JPG = '.jpg'
    TEST_IMAGE_GIF = '.gif'
    TEST_IMAGE_WEBP = '.webp'

    def setUp(self):
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'photo_for_testing.jpg'

        user1 = User.objects.create_user(username='test', password="qwerty")
        user1.save()
        self.user1_token = user1.auth_token

        self.photo = Photo.objects.create(owner=user1, name='NewPhoto1', file_name=file_mock.name)
        self.photo2 = Photo.objects.create(owner=user1, name='NewPhoto2', file_name=file_mock.name)

        image = io.BytesIO()
        Image.new('RGB', (640, 480)).save(image, 'JPEG')
        image_file = SimpleUploadedFile(self.TEST_IMAGE_NAME + self.TEST_IMAGE_JPG, image.getvalue())

        self.data = {
            "name": "MyPhoto",
            "file_name": image_file
        }

    def tearDown(self):
        temp_img_path = os.path.join(settings.MEDIA_PATH, self.TEST_IMAGE_NAME + self.TEST_IMAGE_JPG)
        temp_thumb_path = os.path.join(settings.THUMBS_PATH, self.TEST_IMAGE_NAME + self.TEST_IMAGE_WEBP)
        if os.path.exists(temp_img_path):
            os.remove(temp_img_path)
        if os.path.exists(temp_thumb_path):
            os.remove(temp_thumb_path)

    def test_list_site_photos_success(self):
        response = self.client.get(reverse('photo_list_all'))
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_no_id_photo_fault(self):
        response = self.client.get(reverse('photo_retrieve', kwargs={'pk': 111}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_photo_success(self):
        serializer_data = PhotoSerializer(self.photo).data
        v = serializer_data['viewed']
        response = self.client.get(reverse('photo_retrieve', kwargs={'pk': 1}))
        self.assertEqual(v+1, response.data['viewed'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_photo_fault(self):
        response = self.client.post(reverse('user_photo_list_create'), self.data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_upload_photo_wrong_format_fault(self):
        image = io.BytesIO()
        Image.new('RGB', (640, 480)).save(image, 'JPEG')
        upload_gif = {
            "name": "MyPhoto",
            "file_name": SimpleUploadedFile(self.TEST_IMAGE_NAME + self.TEST_IMAGE_GIF, image.getvalue())
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.user1_token))
        response = self.client.post(reverse('user_photo_list_create'), upload_gif, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_oversized_photo_fault(self):
        big_image = io.BytesIO()
        Image.new('RGB', (20000, 18000)).save(big_image, 'JPEG')
        print(f'Big image size: {len(big_image.getvalue())} bytes')
        upload_big = {
            "name": "MyBigPhoto",
            "file_name": SimpleUploadedFile(self.TEST_IMAGE_NAME + self.TEST_IMAGE_JPG, big_image.getvalue())
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.user1_token))
        response = self.client.post(reverse('user_photo_list_create'), upload_big, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_photo_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.user1_token))
        response = self.client.post(reverse('user_photo_list_create'), self.data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_users_photos_fault(self):
        response = self.client.get(reverse('user_photo_list_create'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_users_photos_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.user1_token))
        response = self.client.get(reverse('user_photo_list_create'))
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_users_photo_fault(self):
        response = self.client.get(reverse('user_photo_get_patch', kwargs={'pk': self.photo.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_users_photo_success(self):
        serializer_data = PhotoSerializer(self.photo).data
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.user1_token))
        response = self.client.get(reverse('user_photo_get_patch', kwargs={'pk': self.photo.id}))
        self.assertEqual(serializer_data['name'], response.data['name'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_users_photo_name_fault(self):
        response = self.client.patch(reverse('user_photo_get_patch', kwargs={'pk': self.photo.id}),
                                     {"name": 'new_name'}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_users_photo_name_success(self):
        new_name = "New photo name"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.user1_token))
        response = self.client.patch(reverse('user_photo_get_patch', kwargs={'pk': self.photo.id}),
                                     {"name": new_name}, format='multipart')
        self.assertEqual(new_name, response.data['name'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
