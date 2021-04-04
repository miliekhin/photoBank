from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from api.v1.appAuth.serializer import UserSignUpSerializer


class UsersSignUpView(ModelViewSet):
    """ Регистрация пользователя """
    serializer_class = UserSignUpSerializer
    queryset = User.objects.all()


class UsersLogOutView(APIView):
    """Юзер выходит"""
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
