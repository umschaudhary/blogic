from rest_framework import serializers
from rest_framework_jwt.compat import Serializer


class PhoneNumberSerializer(Serializer):
    """ phone number serializers used for otp generation"""

    phone_number = serializers.CharField(
        max_length=15
    )
