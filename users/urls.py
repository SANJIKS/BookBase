from django.urls import path
from .views import MeView, PinCodeVerificationView, RegistrationView, CustomUserViewSet, CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView, LoginView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('set_password/', CustomUserViewSet.as_view({'post': 'set_password'}), name='user-set-password'),
    path('reset_password/', CustomUserViewSet.as_view({'post': 'reset_password'}), name='user-reset-password'),
    path('reset_password_confirm/', CustomUserViewSet.as_view({'post': 'reset_password_confirm'}), name='user-reset-password-confirm'),
    path('update_me/', MeView.as_view(), name='user-me'),
    path('me/', CustomUserViewSet.as_view({'get': 'me', 'put': 'me', 'delete': 'me'}), name='user-me'),
    path('jwt/create/', CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path('jwt/refresh/', CustomTokenRefreshView.as_view(), name="jwt-refresh"),
    path('jwt/verify/', CustomTokenVerifyView.as_view(), name="jwt-verify"),
    path('pin/verify/', PinCodeVerificationView.as_view(), name='verify-pin'),
    path('login/', LoginView.as_view(), name='login-view'),
]
