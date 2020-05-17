from datetime import datetime
from django.contrib.auth.signals import user_logged_in

from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings


def jwt_response_payload_handler(token, user=None, request=None):
    if user and request:
        user_logged_in.send(sender=user.__class__, request=request, user=user)
    return {
        'token': token,
    }


def get_jwt_token_response(request=None, login_data=None):
    """
    Jwt implementation to get token response
    :param login_data: data to pass for web token serializer
    :param request:
    :return: api token
    """
    if not login_data:
        if not (
            request and ['phone_number', 'password'] in request.data.keys()
        ):
            return Response({
                'error': 'Login Data is required or request should have phone number and password'
            },
                status=status.HTTP_400_BAD_REQUEST)

    serializer = JSONWebTokenSerializer(data=login_data)

    if serializer.is_valid():
        user = serializer.object.get('user') or request.user
        token = serializer.object.get('token')
        response_data = jwt_response_payload_handler(token, user, request)
        response = Response(response_data)
        if api_settings.JWT_AUTH_COOKIE:
            expiration = (datetime.utcnow() +
                          api_settings.JWT_EXPIRATION_DELTA)
            response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                token,
                                expires=expiration,
                                httponly=True)
        return response

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
