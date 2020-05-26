from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.api.v1.mixins.viewset import CreateListRetrieveUpdateViewSet
from apps.api.v1.mixins.serializer import DummySerializer
from apps.posts.models import Post
from apps.posts.models import PostLike
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

    @action(methods=['POST'], detail=True,
            permission_classes=[IsAuthenticated],
            serializer_class=DummySerializer,
            url_name='like-unlike',
            url_path='like-unlike'
            )
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user
        post_like, created = PostLike.objects.get_or_create(
            post=post, user=user)
        if not created:
            if post_like.liked:
                post_like.liked = False
            else:
                post_like.liked = True
            post_like.save()
        return Response({'liked': post_like.liked})
