#  from django.contrib.auth import get_user_model
#  from django.conf import settings
#
#  from rest_framework import status
#  from rest_framework.response import Response
#  from rest_framework.generics import CreateAPIView
#
#  from apps.users.api.v1.serializers.auth import PhoneNumberSerializer
#  from apps.api.v1.utils.otp_throttle import OTPRateThrottle
#  from apps.commons.constants import SUCCESS
#
#
#  USER = get_user_model()
#
#
#  class OTPGenerateView(CreateAPIView):
#      """ create phone otp """
#
#      serializer_class = PhoneNumberSerializer
#      permission_classes = []
#      throttle_classes = [OTPRateThrottle, ]
#
#      def create(self, request, *args, **kwargs):
#          serializer = self.get_serializer(data=request.data)
#          serializer.is_valid(raise_exception=True)
#          try:
#              user = USER.objects.get(**serializer.data)
#
#              can_generate, reason = user.can_generate_otp()
#              if not can_generate:
#                  return Response(
#                      data={'error': reason},
#                      status=status.HTTP_400_BAD_REQUEST
#                  )
#
#              generation_status, message = user.generate_otp()
#              if generation_status == SUCCESS:
#                  if settings.DEBUG:
#                      return Response(
#                          status=status.HTTP_201_CREATED,
#                          data={'otp': message}
#                      )
#                  else:
#                      return Response(status=status.HTTP_201_CREATED)
#              else:
#                  return Response(
#                      data={'error': message},
#                      status=status.HTTP_400_BAD_REQUEST
#                  )
#          except USER.MultipleObjectsReturned:
#              return Response(
#                  data={'error': 'Some error occured.'},
#                  status=status.HTTP_400_BAD_REQUEST
#              )
#          except USER.DoesNotExist:
#              return Response(
#                  data={'error': 'User Doesn\'t Exists.'},
#                  status=status.HTTP_400_BAD_REQUEST
#              )
