from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class UserSignUpSerializer(ModelSerializer):
    auth_token = SerializerMethodField()
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'auth_token')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        return user

    def get_auth_token(self, obj):
        """ Получаем токен юзера """
        try:
            token = obj.auth_token
        except ObjectDoesNotExist:
            token = ''
        return str(token)
