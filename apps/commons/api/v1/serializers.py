from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from apps.api.v1.mixins.serializer import DynamicFieldsModelSerializer
from apps.commons.utils.validators import validate_name
from apps.commons.models.common import Category


class CategorySerializer(DynamicFieldsModelSerializer):
    name = serializers.CharField(
        max_length=50, validators=[
            validate_name, UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        model = Category
        fields = "__all__"
