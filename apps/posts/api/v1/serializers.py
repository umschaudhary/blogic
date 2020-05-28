from rest_framework import serializers
from apps.api.v1.mixins.serializer import DynamicFieldsModelSerializer
from apps.posts.models import Post
from apps.commons.api.v1.serializers import CategorySerializer


class PostSerializer(DynamicFieldsModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    total_likes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_fields(self):
        fields = super().get_fields()
        if self.request and self.request.method.lower() == 'get':
            fields['category'] = CategorySerializer(
                fields=['id', 'name']
            )
        return fields

    def get_total_likes(self, obj):
        return obj.likes.count()

    def get_total_comments(self, obj):
        return obj.comments.filter(active=True).count()
