from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserViewSet
from drf_yasg.utils import swagger_auto_schema

from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.views import APIView

from rest_framework import generics
from rest_framework.response import Response

from .models import PhoneVerificationCode, CustomUser
from decouple import config
from .serializers import LoginSerializer, PasswordLoginSerializer, PasswordResetConfirmSerializer, PasswordResetSerializer, PinCodeVerificationSerializer, RegistrationSerializer, CustomUserSerializer, CustomUserPatchSerializer, ResendVerificationCodeSerializer


User = get_user_model()

class RegistrationView(APIView):
    @swagger_auto_schema(
        operation_summary="Регистрация",
        operation_description="Эндпоинт для регистрации нового пользователя. Отправляет пин-код на указанный номер телефона.",
        request_body=RegistrationSerializer,
        responses={
            201: openapi.Response(
                description="Пользователь создан и пин-код отправлен на номер телефона.",
                examples={
                    "application/json": {"detail": "Пользователь создан и пин-код отправлен на номер телефона."}
                }
            ),
            200: openapi.Response(
                description="Пин-код отправлен на номер телефона.",
                examples={
                    "application/json": {"detail": "Пин-код отправлен на номер телефона."}
                }
            ),
            400: openapi.Response(
                description="Неверный запрос.",
                examples={
                    "application/json": {"phone_number": "Пользователь с таким номером телефона уже существует и активирован."}
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            name = serializer.validated_data['name']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(phone_number=phone_number)
                if user.is_active:
                    return Response(
                        {"phone_number": "Пользователь с таким номером телефона уже существует и активирован."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    user.name = name
                    user.set_password(password)
                    user.save()

                    verification_code = PhoneVerificationCode.objects.create(user=user)
                    verification_code.generate_and_send_code()

                    return Response({"detail": "Пользователь создан и пин-код отправлен на номер телефона."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    phone_number=phone_number,
                    name=name,
                    password=password
                )
                verification_code = PhoneVerificationCode.objects.create(user=user)
                verification_code.generate_and_send_code()
                return Response({"detail": "Пользователь создан и пин-код отправлен на номер телефона."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_summary='Авторизация',
        operation_description='Эндпоинт для получения access и refresh токена'
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_summary='JWT Refresh',
        operation_description='This endpoint is used for refreshing JWT token'
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        operation_summary='JWT Verify',
        operation_description='This endpoint is used for verifying JWT token'
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomUserViewSet(DjoserViewSet):
    @swagger_auto_schema(operation_summary='Мой аккаунт', operation_description="This endpoints is used for edit user's account")
    def me(self, request, *args, **kwargs):
        if request.method == 'PATCH':
            serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return super().me(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary='Сменить пароль', operation_description='This endpoint is used for setting user password')
    @action(["post"], detail=False)
    def set_password(self, request, *args, **kwargs):
        return super().set_password(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary='Восстановить пароль', operation_description='This endpoint is used for resetting user password')
    @action(["post"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        return super().reset_password(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary='Восстановить пароль (Confirm)', operation_description='This endpoint is used for confirming password reset')
    @action(["post"], detail=False)
    def reset_password_confirm(self, request, *args, **kwargs):
        return super().reset_password_confirm(request, *args, **kwargs)
    


class PinCodeVerificationView(generics.CreateAPIView):
    serializer_class = PinCodeVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_data = serializer.save()
        return Response(token_data, status=status.HTTP_200_OK)
    

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()
        return Response(response_data, status=status.HTTP_200_OK)
    

class MeView(APIView):

    @swagger_auto_schema(operation_summary='Мой аккаунт', operation_description="Эндпоинт для редактирования аккаунта пользователя", request_body=CustomUserSerializer)
    def patch(self, request, *args, **kwargs):
        serializer = CustomUserPatchSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PasswordLoginView(APIView):
    serializer_class = PasswordLoginSerializer

    @swagger_auto_schema(operation_summary='Логин через пароль', operation_description='Эндпоинт для логина с паролем', request_body=PasswordLoginSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ResendVerificationCodeView(APIView):
    @swagger_auto_schema(
        operation_summary="Повторная отправка SMS",
        operation_description="Эндпоинт для повторной отправки SMS кода подтверждения.",
        request_body=ResendVerificationCodeSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = ResendVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        user = CustomUser.objects.get(phone_number=phone_number)
        verification_code = PhoneVerificationCode.objects.create(user=user)
        verification_code.generate_and_send_code()
        return Response({"detail": "Пин-код отправлен на номер телефона."}, status=status.HTTP_200_OK)


class PasswordResetView(APIView):
    @swagger_auto_schema(
        operation_summary="Сброс пароля",
        operation_description="Эндпоинт для отправки кода на номер телефона для сброса пароля.",
        request_body=PasswordResetSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        user = CustomUser.objects.get(phone_number=phone_number)
        verification_code = PhoneVerificationCode.objects.create(user=user)
        verification_code.generate_and_send_code()
        return Response({"detail": "Код для сброса пароля отправлен на номер телефона."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    @swagger_auto_schema(
        operation_summary="Подтверждение сброса пароля",
        operation_description="Эндпоинт для установки нового пароля с помощью кода подтверждения.",
        request_body=PasswordResetConfirmSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        new_password = serializer.validated_data['new_password']
        user = CustomUser.objects.get(phone_number=phone_number)
        user.set_password(new_password)
        user.save()
        return Response({"detail": "Пароль успешно изменен."}, status=status.HTTP_200_OK)
