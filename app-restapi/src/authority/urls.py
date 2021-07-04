from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authority import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('user/', views.AuthUserAPIView.as_view(), name='user'),
    path('email-verify/', views.VerifyUserEmail.as_view(), name='email-verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('password-reset/', views.PasswordResetEmailAPIView.as_view(), name='password-reset'),
    path('password-reset/<uidb64>/<token>/', views.PasswordTokenCheckAPIView.as_view(), name='password-reset-check'),
    path('password-reset-complete/', views.SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
]