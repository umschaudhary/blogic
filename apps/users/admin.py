from django.contrib import admin
from apps.users.models import User, PhoneOtp

admin.site.register([User, PhoneOtp])
