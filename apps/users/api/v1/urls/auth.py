from django.urls import path
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)
from apps.users.api.v1.views.auth import OTPGenerateView, OTPVerifyView

app_name = 'auth'

urlpatterns = [
    path('get-token/', obtain_jwt_token, name='get_token'),
    path('refresh-token/', refresh_jwt_token, name='refresh_token'),
    path('verify-token/', verify_jwt_token, name='verify_token'),
    path('generate-otp/', OTPGenerateView.as_view(), name='generate_otp'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify_otp'),
]
