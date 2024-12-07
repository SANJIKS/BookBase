from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, PhoneVerificationCode

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'phone_number', 'name', 'password')

class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'avatar', 'email', 'name', 'phone_number')

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)

        instance.save()
        print("User instance after update:", instance)
        return instance
    
class CustomUserPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['avatar', 'email', 'name', 'phone_number']
    

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['phone_number', 'name', 'password']
        write_only_fields = ('password',)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')

        user = CustomUser.objects.filter(phone_number=phone_number).first()

        if user and user.is_active:
            raise serializers.ValidationError("Пользователь с таким номером телефона уже существует и активирован.")
        
        if user and not user.is_active:
            pass
        
        return attrs
    

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, value):
        try:
            user = CustomUser.objects.get(phone_number=value)
            if not user.is_active:
                raise serializers.ValidationError("Пользователь не активирован.")
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким номером телефона не найден. Пожалуйста, зарегистрируйтесь.")
        return value

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        user = CustomUser.objects.get(phone_number=phone_number)
        verification_code = PhoneVerificationCode.objects.create(user=user)
        verification_code.generate_and_send_code()
        return {"detail": "Пин-код отправлен на номер телефона."}
    
    
class PinCodeVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        code = attrs.get('code')

        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Неверный номер телефона или код.")

        verification_code = PhoneVerificationCode.objects.filter(user=user).latest('created_at')
        if not verification_code.verify_code(code):
            raise serializers.ValidationError("Неверный номер телефона или код.")

        if not user.is_active:
            user.is_active = True
            user.save()


        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
class PasswordLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        if phone_number and password:
            user = authenticate(phone_number=phone_number, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("Аккаунт не активирован.")
                return {
                    'refresh': str(RefreshToken.for_user(user)),
                    'access': str(RefreshToken.for_user(user).access_token)
                }
            else:
                raise serializers.ValidationError("Неверный телефон или пароль.")
        else:
            raise serializers.ValidationError("Необходимо указать телефон и пароль.")
        

class ResendVerificationCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate(self, data):
        phone_number = data.get('phone_number')
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            if user.is_active:
                raise serializers.ValidationError("Пользователь уже активирован.")
            return data
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким номером телефона не найден.")


class PasswordResetSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate(self, data):
        phone_number = data.get('phone_number')
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            if not user.is_active:
                raise serializers.ValidationError("Аккаунт не активирован.")
            return data
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким номером телефона не найден.")

class PasswordResetConfirmSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        phone_number = data.get('phone_number')
        code = data.get('code')
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            verification_code = PhoneVerificationCode.objects.filter(user=user).latest('created_at')
            if not verification_code.verify_code(code):
                raise serializers.ValidationError("Неверный код.")
            return data
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким номером телефона не найден.")
