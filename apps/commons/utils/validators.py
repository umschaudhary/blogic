from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import serializers


def validate_otp(otp):
    """
    Validate Otp
    :param otp:
    :return:
    """
    otp = str(otp)
    otp_length = settings.OTP_SETTINGS.get("OTP_LENGTH")

    if not len(otp) == otp_length:
        raise serializers.ValidationError(
            _(f'Otp should have length of {otp_length}')
        )
    return otp
