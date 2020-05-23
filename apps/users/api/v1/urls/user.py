from django.urls import path
from rest_framework import routers
from apps.users.api.v1.views.user import (
    UserViewSet,
    UserPasswordChangeView,
    UserPasswordSetAPIView
)

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    path('change-password/', UserPasswordChangeView.as_view(),
         name='change-password'),
    path('set-password/', UserPasswordSetAPIView.as_view(),
         name='set-password'),
]

urlpatterns += router.urls
