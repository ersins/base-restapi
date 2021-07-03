import jwt
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework import response, status, permissions
from rest_framework.generics import GenericAPIView

from authority.serializers import RegisterSerializer, LoginSerializer

user_model = get_user_model()

class AuthUserAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return response.Response({'user': serializer.data})


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserEmail(GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = user_model.objects.get(id=payload['user_id'])
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

            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response({'message': 'Invalid credentials, try again'}, status=status.HTTP_401_UNAUTHORIZED)
