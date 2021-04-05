from django.urls import path
from .views import slider_site, slider_user

urlpatterns = [
    path('site/', slider_site, name='site_slideshow'),
    path('user/<int:user_id>/', slider_user, name='user_slideshow'),
]
