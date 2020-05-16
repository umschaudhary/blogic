#  import uuid
#  import hashlib
#  import hmac
#  import struct
#
#  from django.conf import settings
#  from apps.common.utils.sms import send_sms
#
#
#  def dt(mac):
#      hdig = mac.hexdigest()
#      offset = int(hdig[-1], 16)
#      p = hdig[offset * 2: offset * 2 + 8]
#      return int(p, 16) & 0x7fffffff
#
#
#  def hotp(key, counter=0, token_length=5):
#      """Generate an HOTP token.
#      ``k``
#          Key; bytestring of length 20.
#      ``c``
#          Counter; integer in range 0 .. 2**64 - 1
#      ``n``
#          Token length; integer in {6,7,8}
#      """
#      mac = hmac.new(key, struct.pack(">Q", counter), hashlib.sha1)
#      s = dt(mac)
#      return "{:05}".format(s % 10 ** token_length)
#
#
#  def generate_random_otp_code():
#      """
#      :return: random otp
#      :rtype: str
#      """
#      key = f"{uuid.uuid4().hex}"[:20].encode()
#      return hotp(key)
#
#
#  def send_otp(phone_number):
#      """
#      Send sms to specified Phone Number with otp
#      :param str phone_number:
#      :return: otp, status('Success' or 'Failed')
#      :rtype: str
#      """
#      otp = generate_random_otp_code()
#
#      otp = str(otp)
#
#      message = """
#      Your OTP has been generated.
#      {}
#      """.format(otp)
#
#      status = send_sms(phone_number, message)
#      return status, otp
