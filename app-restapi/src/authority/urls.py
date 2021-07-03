from django.urls import path

from authority import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('user/', views.AuthUserAPIView.as_view(), name='user'),
    path('email-verify/', views.VerifyUserEmail.as_view(), name='email-verify'),
]