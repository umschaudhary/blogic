from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from apps.api.v1.mixins.viewset import CreateListRetrieveUpdateViewSet
from apps.posts.models import Post
from apps.posts.api.v1.serializers import PostSerializer
from apps.commons.utils.permission_classes import (
    ManagerPermission,
    IsOwnerOrManager,
)


class PostViewSet(CreateListRetrieveUpdateViewSet):
    """
    list, create, update and retrieve viewset for  Posts
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    filter_fields = ('category', )
    search_fields = ['title', 'author__full_name', ]
    ordering_fields = (
        'view_count',
        'created_at',
        'modified_at',
        'deadline'
    )
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [AllowAny],
        'update': [IsOwnerOrManager],
        'retrieve': [AllowAny],
        'partial_update': [IsOwnerOrManager]
    }

    def get_permissions(self):
        """ Permission setup """
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance.view_count += 1
        instance.save()
        return Response(serializer.data)
