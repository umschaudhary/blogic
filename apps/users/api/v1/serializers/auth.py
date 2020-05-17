from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_jwt.compat import Serializer

from apps.commons.utils.validators import validate_otp
from apps.commons.utils.helper_classes import DummyObject

USER = get_user_model()


class PhoneNumberSerializer(Serializer):
    """ phone number serializers used for otp generation"""

    phone_number = serializers.CharField(
        max_length=15
    )


class OTPVerificationSerializer(Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=5, validators=[validate_otp])

    def validate(self, data):
        validated_data = super().validate(data)
        try:
            phone_number = validated_data.get('phone_number')
            otp = validated_data.get('otp')
            user = USER.objects.get(phone_number=phone_number)
            valid, reason = user.is_valid_otp(otp, update_try_count=True)
            user.is_active = True
            user.save()
            if valid:
                return {
                    'phone_number': phone_number,
                    'otp': otp
                }
            else:
                raise serializers.ValidationError({'otp': reason})
        except USER.DoesNotExist:
            raise serializers.ValidationError(
                _("User Doesn't Exists.")
            )

    def create(self, validated_data):
        return DummyObject(**validated_data)
