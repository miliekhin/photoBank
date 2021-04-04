from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from PIL import Image
import os

# Делаем поле имейла юзера обязательным для заполниения
User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if kwargs['raw']:
        # выходим если приходит фикстура юзера
        return
    if created:
        Token.objects.create(user=instance)


class Photo(models.Model):

    def create_thumbnail(self):
        src_image = os.path.join(settings.MEDIA_PATH, self.file_name.name)
        target_image = os.path.join(
            settings.THUMBS_PATH,
            os.path.splitext(self.file_name.name)[0] + '.webp'
        )
        os.makedirs(os.path.dirname(target_image), exist_ok=True)
        image = Image.open(src_image)
        if any(size > settings.IMAGE_MAX_SIZE_PX for size in image.size):
            image.thumbnail(size=(settings.IMAGE_MAX_SIZE_PX, settings.IMAGE_MAX_SIZE_PX))
        image = image.convert('RGB')
        image.save(target_image, 'webp')

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)
        self.create_thumbnail()

    owner = models.ForeignKey(User, null=False, related_name='photo', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    file_name = models.ImageField()
    created = models.DateTimeField(auto_now_add=True)
    viewed = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'id: {self.id} - {self.name}'


class UserTopNotifyMessage(models.Model):
    """Сообщение юзеру о том что его фото в топ 3 сайта"""
    subject = models.CharField(max_length=256, blank=False, null=True)
    from_email = models.EmailField(default=settings.SERVER_EMAIL)
    message = models.TextField(max_length=512, blank=False, null=True)

    class Meta:
        verbose_name = "Сообщение топ юзерам"
        verbose_name_plural = "Сообщения топ юзерам"

    def __str__(self):
        return 'Сообщение c поздравлением'
