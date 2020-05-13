
from django.urls import path, include

app_name = "api_v1"

urlpatterns = [
    path('users/', include('apps.users.api.v1.urls')),
]
