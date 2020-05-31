from django.db import models
from django.contrib.auth import get_user_model
from apps.commons.models.abstract_base import BaseModel, SlugModel
from apps.commons.models.common import Category
from apps.commons.utils.helpers import get_upload_path
from apps.posts.constants import (
    STATUS_CHOICES,
    PRIVACY_CHOICES,
    PUBLIC,
    PUBLISHED
)


User = get_user_model()


class Post(BaseModel):
    scheduled_for = models.DateTimeField(null=True)
    category = models.ForeignKey(
        Category, related_name='posts',
        on_delete=models.CASCADE
    )

    attachment = models.FileField(
        upload_to=get_upload_path,
        null=True,
        blank=True
    )
    body = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(null=True)
    status = models.CharField(
        choices=STATUS_CHOICES, default=PUBLISHED, max_length=50,
        db_index=True
    )
    privacy = models.CharField(
        choices=PRIVACY_CHOICES, default=PUBLIC, max_length=50
    )
    view_count = models.PositiveIntegerField(default=0)

    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='posts'
    )
    total_likes = models.PositiveIntegerField(default=0)
    total_comments = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('created_at', )

    def __str__(self):
        return f"post by {self.author}"


class PostLike(BaseModel):
    """
    Posts like model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='likes')
    liked = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'post')


class Comment(BaseModel):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=True, max_length=1000)
    image = models.ImageField(
        upload_to=get_upload_path, blank=True, null=True,
    )
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.SET_NULL)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return 'Comment by {}'.format(self.user)
