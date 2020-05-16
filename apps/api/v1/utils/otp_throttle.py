from django.conf import settings
from rest_framework.throttling import UserRateThrottle


class OTPRateThrottle(UserRateThrottle):
    scope = 'otp'

    def allow_request(self, request, view):
        ip_address = request.META['REMOTE_ADDR']
        whitelisted_ips = getattr(
            settings, 'WHITELISTED_IPS_FOR_THROTTLING', [])
        if ip_address in whitelisted_ips:
            return True
        else:
            return super().allow_request(request, view)
