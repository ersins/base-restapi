import smtplib

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template


@shared_task
def send_activation_mail(data):
    """
    Kullanıcı aktivasyonu için kullanılan celery task fonksiyonu post_save_user_create_reciever signals tarafından kullanılır
    :param email_activation_id:
    :return:
    """

    # base_url = getattr(settings, 'BASE_URL', 'https://www.ersins.com')
    # key_path = reverse("account:email-activate", kwargs={'key': email_activation_obj.key})  # use reverse
    # path = "{base}{path}".format(base=base_url, path=key_path)
    context = {
        # 'path': path,
        'path': data['url'],
        'email': data['user'].email
    }
    txt_ = get_template("registration/emails/verify.txt").render(context)
    html_ = get_template("registration/emails/verify.html").render(context)
    subject = 'Email Verification'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [data['user'].email]
    try:
        sent_mail = send_mail(
            subject,
            txt_,
            from_email,
            recipient_list,
            html_message=html_,
            fail_silently=False,
        )
    except smtplib.SMTPAuthenticationError as ex:
        # TODO log edilecek
        print(ex)
