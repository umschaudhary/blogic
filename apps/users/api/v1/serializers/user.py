from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_jwt.compat import PasswordField
from rest_framework.fields import ReadOnlyField

from apps.api.v1.mixins.serializer import DynamicFieldsModelSerializer, DummySerializer
from apps.commons.utils.helper_classes import DummyObject
from apps.commons.utils.validators import validate_otp
from apps.users.models import PhoneOtp

User = get_user_model()


class UserSerializer(DynamicFieldsModelSerializer):
    """ User Serializers for UserViewSet """
    password = serializers.CharField(max_length=25, min_length=8)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "phone_number",
            "password",
            "email",
            "full_name",
            "gender",
            "is_blocked",
            "profile_picture"
        ]

    def get_fields(self):
        fields = super().get_fields()
        if self.request and self.request.method.lower() == 'get':
            fields['password'] = serializers.HiddenField(default=None)
            fields['profile_picture'] = serializers.SerializerMethodField()
        return fields

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = super().create(validated_data)
        instance.set_password(password)
        instance.is_active = False
        instance.save()
        return instance

    def get_profile_picture(self, obj):
        logo_path = obj.profile_picture.url if obj.profile_picture else \
            '/media/uploads/post/avatar.jpg'
        return self.request.build_absolute_uri(logo_path)


class PasswordChangeSerializer(DummySerializer):
    old_password = PasswordField(max_length=25, min_length=5, write_only=True)
    password = PasswordField(max_length=25, min_length=5, write_only=True)
    confirm_password = PasswordField(
        max_length=25, min_length=5, write_only=True)
    message = ReadOnlyField(default="Password Changed Successfully")

    def validate(self, attrs):
        request = self.context.get('request')

        if not request and request.user:
            raise serializers.ValidationError(('Some Error Occurred.'))
        old_password = attrs.get('old_password')

        if not request.user.check_password(old_password):
            raise serializers.ValidationError(
                {"old_password": ('Old Password is incorrect.')})
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if old_password == password:
            raise serializers.ValidationError(
                {"password": "New Password can't be same as old password."})

        if password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Confirm Password doesn't matches. "})
        return attrs

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        instance.set_password(password)
        instance.save()
        return DummyObject(**validated_data)


class PasswordSetSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=25)
    password = PasswordField(max_length=25, min_length=5)
    confirm_password = PasswordField(max_length=25, min_length=5)
    otp = serializers.CharField(max_length=5,
                                validators=[validate_otp])

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        otp = attrs.get('otp')
        valid, reason = PhoneOtp.is_valid_otp(
            phone_number,
            otp,
            for_password_set=True,
            update_try_count=True
        )
        if not valid:
            raise serializers.ValidationError(reason)
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Confirm Password doesn't matches with password."}
            )
        return attrs

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        instance.set_password(password)
        instance.is_active = True
        instance.save()
        return DummyObject(**validated_data)
