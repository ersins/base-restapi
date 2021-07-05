from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [settings.APP_SCHEME, 'http', 'https']

