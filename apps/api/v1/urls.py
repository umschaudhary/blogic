
from django.conf import settings
from django.urls import path, include

app_name = "api_v1"

urlpatterns = [
    path('auth/', include('apps.users.api.v1.urls.auth')),
    path('users/', include('apps.users.api.v1.urls.user')),
    path('posts/', include('apps.posts.api.v1.urls')),
    path('commons/', include('apps.commons.api.v1.urls')),
]
