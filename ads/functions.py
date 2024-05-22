from datetime import date, datetime
from _decimal import Decimal
from geolite2 import geolite2
import json


def get_user_data(request):
    data = {}

    data['operating_system'] = request.META.get('HTTP_SEC_CH_UA_PLATFORM')
    data['user_agent'] = request.META.get('HTTP_USER_AGENT')
    data['ip_address'] = request.META.get('REMOTE_ADDR')
    data['referrer'] = request.META.get('HTTP_REFERER')

    reader = geolite2.reader()
    resp = reader.get(data['ip_address'])
    data['geolocation'] = json.dumps(resp['continent']['names']['en'],
                                     indent=4) if resp else ''

    return data

def custom_serializer(obj):
    if isinstance(obj, (datetime, date)):
        serial = obj.isoformat()
        return serial
    if isinstance(obj, Decimal):
        return float(obj)


def generate_colors(n):
    colors = []
    for i in range(n):
        ratio = i / (n - 1) if n > 1 else 0
        red = int(255 * ratio)
        green = int(255 * (1 - ratio))
        blue = 0
        color = f'#{red:02x}{green:02x}{blue:02x}'
        colors.append(color)
    return colors
