from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, JSONParser
from app.models import Photo
from api.v1.photos.serializers import PhotoSerializer, PhotoCreationSerializer, PhotoEditSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class PhotosViewSetAll(ModelViewSet):
    """
    list: Список всех фотографий сайта
    retrieve: Получение конкретной фотографии
    """
    serializer_class = PhotoSerializer
    parser_classes = [JSONParser]
    queryset = Photo.objects.all()

    def retrieve(self, request, pk=None, **kwargs):
        """Получение конкретной фотографии"""
        photo = get_object_or_404(Photo, pk=pk)
        photo.viewed += 1
        photo.save()
        serializer = PhotoSerializer(photo)
        return Response(serializer.data)


class PhotosViewSetUser(ModelViewSet):
    """
    list: Список всех фотографий пользователя
    create: Добавление фотографии. Размер не более 5 Мб. Только JPG, JPEG, PNG форматы.
    partial_update: Изменение имени фотографии
    retrieve: Получение конкретной фотографии пользователя
    """
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return PhotoCreationSerializer
        if self.action == 'partial_update':
            return PhotoEditSerializer

        return PhotoSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.photo.all()
