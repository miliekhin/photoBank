from rest_framework import serializers
from app.models import Photo
from django.conf import settings
import os


class PhotoSerializer(serializers.ModelSerializer):
    """Сериалайзер получения картинок"""
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = '__all__'

    def get_thumbnail(self, obj):
        return f'{settings.THUMBS_URL}{os.path.splitext(obj.file_name.name)[0]}.webp'


class PhotoCreationSerializer(serializers.ModelSerializer):
    """Сериалайзер добавления фото"""
    class Meta:
        model = Photo
        exclude = ('owner', 'viewed')

    @staticmethod
    def validate_file_name(value):
        if os.path.splitext(value.name)[1].lower() not in settings.ALLOWED_IMAGE_EXT:
            raise serializers.ValidationError({'error': 'Разрешены только файлы формата PNG и JPEG '})

        if value.size > settings.IMAGE_FILE_MAX_SIZE:
            raise serializers.ValidationError({'error': 'Размер файла не должен превышать 5 МБ.'})
        return value


class PhotoEditSerializer(serializers.ModelSerializer):
    """Сериалайзер для изменения названия картинки"""
    class Meta:
        model = Photo
        fields = ('id', 'name',)
