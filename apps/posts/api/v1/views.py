from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.api.v1.mixins.viewset import CreateListRetrieveUpdateViewSet
from apps.api.v1.mixins.serializer import DummySerializer
from apps.posts.models import Post, PostLike, Comment
from apps.posts.api.v1.serializers import PostSerializer, CommentSerializer
from apps.posts.api.v1.serializers import CommentPostSerializer
from apps.commons.utils.permission_classes import (
    ManagerPermission,
    IsOwnerOrManager,
)
from apps.commons.utils.permission_mixins import CommonActionPermissionMixin


class PostViewSet(CommonActionPermissionMixin, CreateListRetrieveUpdateViewSet):
    """
    list, create, update and retrieve viewset for  Posts
    """
    queryset = Post.objects.order_by("-modified_at")
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


    @action(methods=['GET'], detail=True,
            url_name='comments',
            url_path='comments',
            serializer_class=CommentSerializer
            )
    def comments(self, request, *args, **kwargs):
        post = self.get_object()
        comments = Comment.objects.filter(post=post, parent_id=None)

        page = self.paginate_queryset(comments)
        if page is not None:
           serializer = self.serializer_class(page, many=True)
           return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data)


class CommentViewSet(CommonActionPermissionMixin, CreateListRetrieveUpdateViewSet):
    """
    list, create, update and retrieve viewset for Comments 
    """
    queryset = Comment.objects.all()
    serializer_class = CommentPostSerializer 
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    filter_fields = ["post", "user"]
