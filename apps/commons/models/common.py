from django.db import models
from apps.commons.models.abstract_base import BaseModel
from apps.commons.utils.helpers import get_upload_path


class Category(BaseModel):
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    name = models.CharField(max_length=50, unique=True, db_index=True)
    icon = models.ImageField(
        upload_to=get_upload_path,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('created_at', )
        constraints = [
            models.UniqueConstraint(
                fields=['parent', 'name'],
                name='unique_category_name_with_parent')
        ]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
