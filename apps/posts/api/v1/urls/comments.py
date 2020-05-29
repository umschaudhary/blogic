from django.conf import settings
from django.urls import path, include
from rest_framework import routers
from apps.posts.api.v1.views import CommentViewSet

app_name = "comments"

router = routers.DefaultRouter()
router.register(r'', CommentViewSet, basename='comments')

urlpatterns = router.urls
