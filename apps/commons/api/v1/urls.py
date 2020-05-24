from django.urls import path
from rest_framework import routers
from apps.commons.api.v1.views import CategoryViewSet

app_name = "commons"

router = routers.DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = router.urls
