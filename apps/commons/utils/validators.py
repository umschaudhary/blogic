import re
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import serializers


PHONE_NUMBER_REGEX = re.compile(r"^(([+]?\d{3})-?)?\d{7,10}$")


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


def is_future_datetime(value, error_message=_("DateTime Must Be Future.")):
    if not timezone.now() < value:
        raise serializers.ValidationError(error_message)
    return value


def validate_name(name):
    if not name.replace(" ", "").isalpha():
        raise serializers.ValidationError(
            _("Name Should not contain any special characters."))
    return name


def validate_phone_number(number):
    phone_number = str(number)

    if not PHONE_NUMBER_REGEX.match(phone_number):
        raise serializers.ValidationError(
            _('Phone Number format is not valid. Some examples of supported'
              ' phone numbers are numbers are 9811111111, 08256666,'
              ' 977-9833333333, +977-9833333333, 977-08256666')
        )

    return number
