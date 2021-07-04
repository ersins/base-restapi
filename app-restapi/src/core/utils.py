from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from core.middleware import RequestMiddleware


def get_create_url(**kwargs):
    absolute_url = ''

    req = RequestMiddleware(get_response=None)
    request = req.thread_local.current_request
    current_domain = get_current_site(request).domain
    relative_link = reverse('email-verify')
    # TODO link oluşturmak için bir yardımcı oluşturulabilir
    absolute_url = f'http://{current_domain}{relative_link}?token={str(token)}'

    return absolute_url