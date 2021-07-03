from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from authority.celery_task import send_activation_mail
from core.middleware import RequestMiddleware

user_model = get_user_model()


# Yeni kullanıcı oluşturulduğunda data kaydından hemen sonra çalışır
# ve eposta aktivasyon mepostası gönderir
@receiver(post_save, sender=user_model)
def post_save_user_create_reciever(sender, instance, created, *args, **kwargs):
    if created:
        token = RefreshToken.for_user(instance).access_token
        req = RequestMiddleware(get_response=None)
        request = req.thread_local.current_request
        current_domain = get_current_site(request).domain
        relative_link = reverse('email-verify')
        # TODO link oluşturmak için bir yardımcı oluşturulabilir
        absolute_url = f'http://{current_domain}{relative_link}?token={str(token)}'
        data = {'url': absolute_url, 'user': instance}
        send_activation_mail(data)
