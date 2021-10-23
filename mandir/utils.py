import urllib
import simplejson as json
from mandir.constants import SMS_API_KEY, GENERIC_MSG, SMS_URL


def send_normal_sms(numbers, message=GENERIC_MSG, sender='TXTLCL'):
    """Will send an sms to end user. """

    data = urllib.parse.urlencode({
        'apikey': SMS_API_KEY,
        'numbers': "91{}".format(numbers),
        'message': message,
        'sender': sender,
        'unicode': "true",
    })
    data = data.encode('utf-8')
    req = urllib.request.Request(SMS_URL, data)
    response = urllib.request.urlopen(req)
    response = json.loads(response.read())

    if response.get('status') != 'success':
        return False

    return True


# def send_normal_tsms(numbers, message_data=GENERIC_MSG):
#     """
#     This will call Tsms services to send an sms to the users.
#     """
#     client = Client(TSMS_KEY, YSMS_DATA)
#     message = {}
#     try:
#         message = client.messages \
#                     .create(body=message_data, from_='+1{}'.format(FROM_DATA), to="+91{}".format(numbers))
#     except TwilioRestException as ex:
#         print ex
#
#     print(message.sid)