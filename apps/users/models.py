import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.utils import timezone

from apps.commons.models.abstract_base import BaseModel
from apps.commons.utils.helpers import get_upload_path
from apps.commons.utils.validators import validate_otp
from apps.users.constants import GENDER_CHOICES
from apps.users.manager import UserManager

# Create your models here.


class User(AbstractUser, BaseModel):

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        default=uuid.uuid4
    )

    full_name = models.CharField(
        _('full name'),
        max_length=150,
        blank=True, null=True
    )

    profile_picture = models.ImageField(
        upload_to=get_upload_path,
        blank=True
    )

    email = models.EmailField(
        _('email address'), null=True,
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )
    phone_number = models.CharField(
        _('phone number'),
        null=True,
        max_length=25,
        error_messages={
            'unique': _("A user with that phone number already exists."),
        },
        unique=True
    )
    gender = models.CharField(
        max_length=20,  # Max length set to 20 considering LGBTQ adding
        choices=GENDER_CHOICES,
        blank=True, null=True
    )

    is_blocked = models.BooleanField(default=False)
    # Remarks is reason for which user is blocked or Unblocked
    remarks = models.CharField(max_length=100, blank=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.full_name} {self.phone_number}'

    def is_manager(self):
        return self.is_active and self.is_staff and self.is_superuser


class PhoneOtp(BaseModel):
    """ PhoneOtp storage """
    user = models.ForeignKey(
        User,
        related_name='otps',
        on_delete=models.CASCADE
    )
    otp = models.CharField(
        _('Otp'), max_length=5,
        validators=[validate_otp], db_index=True
    )
    try_count = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.user} {self.otp}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'otp'], name='unique_user_with_otp'),
        ]

    def update_try_count(self):
        self.try_count += 1
        self.save()

    @classmethod
    def is_valid_otp(cls, user_info,
                     otp, for_password_set=False,
                     update_try_count=False
                     ):
        """
        :param user_info : User Info can be user instance or phone Number
        :param bool for_password_set: Increase Validation time for password reset
        :param bool update_try_count: Increase try count
        :param otp:
        :return: Is otp is valid for given user or Phone Number
        """
        if not all([user_info, otp]):
            return False, _('User Info and OTP is required.')

        phone_otp = PhoneOtp.get_latest_phone_otp(user_info)

        if not phone_otp:
            return False, _("Provided OTP didn't matched.")

        if update_try_count:
            phone_otp.update_try_count()

        if not phone_otp.has_remaining_try:
            return False, _('OTP retry limit reached.')

        if not (phone_otp and phone_otp.otp == otp):
            return False, _("Provided OTP didn't matched.")

        otp_verification_time_limit = phone_otp.created_at + timezone.timedelta(
            seconds=getattr(settings, 'OTP_VERIFICATION_SECONDS', 5 * 60)
        )

        if for_password_set:
            otp_verification_time_limit += timezone.timedelta(
                seconds=getattr(
                    settings,
                    'ACCEPTABLE_TIME_FOR_PASSWORD_SET_AFTER_OTP_GENERATION',
                    10 * 60)
            )

        has_acceptable_time_limit = otp_verification_time_limit >= timezone.now()

        if not has_acceptable_time_limit:
            return False, _('OTP verification time reached.')
        return True

    @classmethod
    def get_latest_phone_otp(cls, user_info):
        """
        :param user_info : User Info can be user instance or phone Number
        :return: PhoneOtp Object
        """
        if not isinstance(user_info, User):
            return cls.objects.filter(user__phone_number=user_info).order_by('-id').first()
        return cls.objects.filter(user=user_info).order_by('-id').first()

    @property
    def remaining_try_count(self):
        return settings.MAX_OTP_RETRY - self.try_count

    @property
    def has_remaining_try(self):
        return self.remaining_try_count > 0
