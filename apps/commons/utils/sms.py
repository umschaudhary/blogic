import requests
import logging

from django.conf import settings

from apps.commons.constants import SUCCESS, FAILED


def send_sms(phone_number, message):
    """
    Send Sms to specified Phone Number
    :param phone_number:
    :param message:
    :return: status ('Success' or 'Failed')
    """
    if settings.SMS_TOKEN is None:
        if not settings.DEBUG:
            # raise error in production
            logging.error('SMS_TOKEN not configured.')
            return FAILED
        return SUCCESS

    # sparrow sms needs 10 digit phone number
    phone_number = str(phone_number).replace('977-', '')
    response = requests.post(
        settings.SMS_URL,
        data={
            'token': settings.SMS_TOKEN,
            'from': settings.SMS_FROM,
            'to': phone_number,
            'text': message
        }
    )

    if response.status_code == 200:
        return SUCCESS
    else:
        logging.error(msg=response.content)
        return FAILED
