from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_jwt.compat import PasswordField
from apps.api.v1.mixins.serializer import DynamicFieldsModelSerializer
from apps.commons.utils.helper_classes import DummyObject

User = get_user_model()


class UserSerializer(DynamicFieldsModelSerializer):
    """ User Serializers for UserViewSet """
    password = serializers.CharField(max_length=25, min_length=8)

    class Meta:
        model = User
        fields = [
            "username",
            "phone_number",
            "password",
            "email",
            "full_name",
            "gender",
            "is_blocked",
            "profile_picture"
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = super().create(validated_data)
        instance.set_password(password)
        instance.save()
        return instance
