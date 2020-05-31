from rest_framework import serializers
from apps.api.v1.mixins.serializer import DynamicFieldsModelSerializer
from apps.posts.models import Post, Comment
from apps.commons.api.v1.serializers import CategorySerializer
from apps.users.api.v1.serializers.user import UserSerializer

class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(
            value,
            context=self.context)
        return serializer.data

class CommentPostSerializer(DynamicFieldsModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), 
    )
    class Meta:
        model = Comment
        fields = ["id", "user", "content", "image", "post"]

    def validate(self, attrs):
        content = attrs.get('content')
        image = attrs.get('image')
        if not content and not image:
            raise serializers.ValidationError("Image Or Comment content Required.")
        return attrs

class CommentSerializer(DynamicFieldsModelSerializer):
    replies = RecursiveField(many=True, read_only=True)
    user = UserSerializer(fields=['id', 'full_name', 'profile_picture'], read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "content", "image", "user", "replies"]


class PostSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"

    def validate(self, attrs):
        attachment = attrs.get('attachment')
        body = attrs.get('body')
        if not attachment and not body:
            raise serializers.ValidationError("Attachment Or Body Required.")
        return attrs

    def get_fields(self):
        fields = super().get_fields()
        if self.request and self.request.method.lower() == 'get':
            fields['category'] = CategorySerializer(
                fields=['id', 'name']
            )
            fields['author'] = UserSerializer(
                    fields=['id', 'full_name', 'profile_picture'],
                    context=self.context)
        if self.request and self.request.method.lower() in  ['post', 'put']:
            fields['author'] = serializers.HiddenField(
                default=serializers.CurrentUserDefault()
            )
        return fields

