from django.urls import path
from rest_framework import routers
from apps.users.api.v1.views.user import UserViewSet

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = router.urls
