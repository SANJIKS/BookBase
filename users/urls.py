from django.urls import path
from .views import MeView, PasswordLoginView, PasswordResetConfirmView, PasswordResetView, PinCodeVerificationView, RegistrationView, CustomUserViewSet, CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView, LoginView, ResendVerificationCodeView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('set_password/', CustomUserViewSet.as_view({'post': 'set_password'}), name='user-set-password'),
    path('update_me/', MeView.as_view(), name='user-me'),
    path('me/', CustomUserViewSet.as_view({'get': 'me', 'put': 'me', 'delete': 'me'}), name='user-me'),
    path('jwt/create/', CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path('jwt/refresh/', CustomTokenRefreshView.as_view(), name="jwt-refresh"),
    path('jwt/verify/', CustomTokenVerifyView.as_view(), name="jwt-verify"),
    path('pin/verify/', PinCodeVerificationView.as_view(), name='verify-pin'),
    path('login/', LoginView.as_view(), name='login-view'),
    path('password_login/', PasswordLoginView.as_view(), name='password-login-view'),
    path('resend-code/', ResendVerificationCodeView.as_view(), name='resend_code'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
