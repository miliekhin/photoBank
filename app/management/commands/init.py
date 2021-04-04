from django.core.management import BaseCommand, call_command
from random import randint
from django.conf import settings
from django.contrib.auth.models import User
from app.models import Photo, UserTopNotifyMessage
import os
from PIL import Image


class Command(BaseCommand):
    help = 'Заполнение БД'

    def handle(self, *args, **kwargs):
        call_command('makemigrations')
        call_command('migrate')
        call_command('flush', verbosity=0, interactive=False)
        call_command('createsuperuser', interactive=False, username='admin', email='test@example.com')
        user = User.objects.get(username='admin')
        user.set_password('admin')
        user.save()

        os.makedirs(settings.MEDIA_PATH, exist_ok=True)
        u1 = User.objects.create(username='user1', email='asdf@werrr.eu')
        u1.set_password('qwerty')
        u1.save()
        u2 = User.objects.create(username='user2', email='bteet@tyrui.eu')
        u2.set_password('qwerty')
        u2.save()

        self.create_images_for_user(u1, 12)
        self.create_images_for_user(u2, 7)
        UserTopNotifyMessage.objects.create(subject='Поздравляем!', message='Ваше фото в топ 3 сайта!!!')
        self.create_photo_for_testing('photo_for_testing.jpg')
        self.stdout.write(self.style.SUCCESS('Project inited.'))

    @staticmethod
    def create_images_for_user(user_obj, count):
        for i in range(count):
            img = Image.new('RGB',
                            (randint(400, 1280), randint(300, 720)),
                            color=(randint(0, 255),
                                   randint(0, 255),
                                   randint(0, 255)))
            file_name = f'picture_{i}_{user_obj.username}.jpg'
            img.save(os.path.join(settings.MEDIA_PATH, file_name))
            Photo.objects.create(
                owner=user_obj,
                name=f'My Photo {user_obj.username} {i}',
                file_name=file_name,
                viewed=randint(0, 12))
            print(f'Photo created: {file_name}')

    @staticmethod
    def create_photo_for_testing(name):
        img = Image.new('RGB',
                        (randint(400, 1280), randint(300, 720)),
                        color=(randint(0, 255),
                               randint(0, 255),
                               randint(0, 255)))
        img.save(os.path.join(settings.MEDIA_PATH, name))
