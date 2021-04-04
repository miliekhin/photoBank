from api.v1.photos.views import PhotosViewSetUser, PhotosViewSetAll
from django.urls import path

urlpatterns = [
    path('', PhotosViewSetAll.as_view({'get': 'list', }), name='photo_list_all'),
    path('<int:pk>/', PhotosViewSetAll.as_view({'get': 'retrieve', }), name='photo_retrieve'),
    path('my/', PhotosViewSetUser.as_view({'post': 'create', 'get': 'list', }), name='user_photo_list_create'),
    path('my/<int:pk>/', PhotosViewSetUser.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='user_photo_get_patch'),
]
