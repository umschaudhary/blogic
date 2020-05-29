from django.conf import settings
from django.urls import path, include
from rest_framework import routers
from apps.posts.api.v1.views import PostViewSet

app_name = "posts"

router = routers.DefaultRouter()
router.register(r'', PostViewSet, basename='posts')

urlpatterns = router.urls
