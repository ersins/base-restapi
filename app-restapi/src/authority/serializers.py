from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import smart_bytes, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers

# from authority.models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from setuptools.unicode_utils import try_encode

from authority.celery_task import send_reset_password_mail, send_reset_password_complete_mail
from core.middleware import RequestMiddleware

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric characters')
        return attrs

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, min_length=8, write_only=True)
    tokens = serializers.SerializerMethodField()
    extra_data = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'tokens', 'extra_data')

        read_only_fields = ['tokens', 'extra_data', ]

    def get_tokens(self, obj):
        user = User.objects.get(email=obj.email)
        return {
            'accesse': user.tokens['access'],
            'refresh': user.tokens['refresh']
        }

    def get_extra_data(self, obj):
        # TODO Mobil için gerekli parametreleri bu alanile gönderilecek
        user = User.objects.get(email=obj.email)
        return {
            'about_me': user.about_me,
        }


class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=6, max_length=100)
    redirect_url = serializers.CharField(max_length=550, required=False)

    class Meta:
        fields = ['email', ]

    def validate(self, attrs):
        email = attrs.get('email', '')
        redirect_url = attrs.get('redirect_url', '')
        qs = User.objects.filter(email=email)
        if qs.exists():
            user = qs.first()
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            req = RequestMiddleware(get_response=None)
            request = req.thread_local.current_request
            # redirect_url=request.data.get('redirect_url')
            current_domain = get_current_site(request).domain
            relative_link = reverse('password-reset-check', kwargs={'uidb64': uidb64, 'token': token})
            # TODO link oluşturmak için bir yardımcı oluşturulabilir
            absolute_url = f'http://{current_domain}{relative_link}?redirect_url={redirect_url}'
            data = {'url': absolute_url, 'user': user, 'subject': 'Reset your password'}
            send_reset_password_mail(data)
            return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=64, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            password = attrs.get('password', '')
            uidb64 = attrs.get('uidb64', '')
            token = attrs.get('token', '')

            user_id = urlsafe_base64_decode(smart_str(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            data = {'user': user, 'subject': 'Şifrenizi başayıyla yenilediniz'}
            send_reset_password_complete_mail(data)

            return user
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
