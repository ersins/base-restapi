from _testcapi import raise_exception

import jwt
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import redirect
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from rest_framework import response, status, permissions
from rest_framework.generics import GenericAPIView

from authority.renderer import UserRenderer
from authority.serializers import RegisterSerializer, LoginSerializer, PasswordResetEmailSerializer, \
    SetNewPasswordSerializer, LogoutSerializer
from helpers.utils import CustomRedirect

User = get_user_model()


class AuthUserAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user.pi.pi
        serializer = RegisterSerializer(user)
        return response.Response({'user': serializer.data})


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserEmail(GenericAPIView):
    authentication_classes = []

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return response.Response({'email': 'Successsfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            raise response.Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            raise response.Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username=email, password=password)

        if user:
            serializer = self.serializer_class(user)
            serializer.data['tokens'] = user.tokens
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response({'message': 'Invalid credentials, try again'}, status=status.HTTP_401_UNAUTHORIZED)


class PasswordResetEmailAPIView(GenericAPIView):
    serializer_class = PasswordResetEmailSerializer
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response({'success': 'We have sent you alink to reset your password'},
                                 status=status.HTTP_200_OK)


class PasswordTokenCheckAPIView(GenericAPIView):
    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(f'{redirect_url}?token_valid=False')
                else:
                    return CustomRedirect(f'{settings.FRONTEND_URL}?token_valid=False')
            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(
                    f'{redirect_url}?token_valid=True?&message=Credentials valid&uidb64={uidb64}&token&{token}')
            else:
                return CustomRedirect(f'{settings.FRONTEND_URL}?token_valid=False')
        except DjangoUnicodeDecodeError as ex:
            return CustomRedirect(f'{redirect_url}?token_valid=False')


class SetNewPasswordAPIView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serialzer = self.serializer_class(data=request.data)
        serialzer.is_valid(raise_exception=True)
        serialzer.save()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
