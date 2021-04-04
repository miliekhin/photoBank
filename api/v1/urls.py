from django.urls import path, include
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('photos/', include('api.v1.photos.urls')),
    path('users/', include('api.v1.appAuth.urls')),
    path('schema/', get_schema_view(
        title="Photo Bank",
        description="Описание API",
        version="1.0.0"
    ), name='openapi-schema'),
]
