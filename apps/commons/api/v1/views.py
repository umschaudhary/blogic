from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.api.v1.mixins.viewset import CreateListRetrieveUpdateViewSet
from apps.posts.models import Post
from apps.posts.api.v1.serializers import PostSerializer
from apps.commons.utils.permission_classes import (
    ManagerWritePermission,
    ManagerPermission,
    IsOwnerOrManager,
)
from apps.commons.api.v1.serializers import CategorySerializer
from apps.commons.models.common import Category


class CategoryViewSet(CreateListRetrieveUpdateViewSet):
    """
    list, create, update and retrieve viewset for categories 
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ['name']
    ordering_fields = (
        'created_at',
        'modified_at',
    )
    permission_classes_by_action = {
        'create': [ManagerWritePermission],
        'list': [AllowAny],
        'update': [ManagerWritePermission],
        'retrieve': [IsAuthenticated],
        'partial_update': [ManagerWritePermission]
    }

    def get_permissions(self):
        """ Permission setup """
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
