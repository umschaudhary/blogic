from django.contrib.admin import ModelAdmin, register
from apps.commons.models.common import Category


@register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', )
