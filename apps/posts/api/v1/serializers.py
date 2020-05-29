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


class CommentSerializer(DynamicFieldsModelSerializer):
    replies = RecursiveField(many=True, read_only=True)
    user = UserSerializer(fields=['id', 'full_name', 'profile_picture'], read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "content", "image", "user", "replies"]

    def get_fields(self):
        fields = super().get_fields()
        if self.request and self.request.method.lower() == 'post':
            fields['user'] = serializers.HiddenField(
                default=serializers.CurrentUserDefault(), 
            )
        return fields

    def validate(self, attrs):
        content = attrs.get('content')
        image = attrs.get('image')
        if not content and not image:
            raise serializers.ValidationError("Image Or Comment content Required.")
        return attrs


class PostSerializer(DynamicFieldsModelSerializer):
    total_likes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()

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

    def get_total_likes(self, obj):
        return obj.likes.count()

    def get_total_comments(self, obj):
        return obj.comments.filter(is_active=True).count()
