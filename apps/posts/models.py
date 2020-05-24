from django.db import models
from django.contrib.auth import get_user_model
from apps.commons.models.abstract_base import BaseModel, SlugModel
from apps.commons.models.common import Category
from apps.commons.utils.validators import is_future_datetime
from apps.commons.utils.helpers import get_upload_path
from apps.posts.constants import (
    STATUS_CHOICES,
    PRIVACY_CHOICES,
    PUBLIC,
    PUBLISHED
)


User = get_user_model()


class Post(SlugModel, BaseModel):
    title = models.CharField(
        max_length=255, db_index=True, unique=True
    )
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
    body = models.TextField(null=True)
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

    class Meta:
        ordering = ('created_at', )
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_with_author')
        ]

    def __str__(self):
        return f"{self.title} by {self.author}"
