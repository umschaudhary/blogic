import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from apps.commons.models.abstract_base import BaseModel
from apps.commons.utils.helpers import get_upload_path
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
