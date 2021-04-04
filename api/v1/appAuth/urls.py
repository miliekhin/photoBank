from rest_framework.authtoken import views as rfa
from api.v1.appAuth.views import UsersSignUpView, UsersLogOutView
from django.urls import path

urlpatterns = [
    path('', UsersSignUpView.as_view({'post': 'create'}), name='signup'),
    path('logout/', UsersLogOutView.as_view(), name='logout'),
    path('login/', rfa.obtain_auth_token, name='login'),
]
