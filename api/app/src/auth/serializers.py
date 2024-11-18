from rest_framework import serializers

from src.user.services.verification_service import is_csrf_valid, is_verification_code_valid
from src.user.services.user_service import get_user_by_email


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    password = serializers.CharField()

    def validate_email(self, value):
        try:
            if value:
                user = get_user_by_email(value)
                if user:
                    raise serializers.ValidationError("User with such email already exists")
            return value
        except Exception as e:
            raise serializers.ValidationError(e)


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()


class RequestPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    code = serializers.UUIDField()
    csrf = serializers.UUIDField()

    def validate_code(self, value):
        return is_verification_code_valid(value)

    def validate_csrf(self, value):
        return is_csrf_valid(value, self.context['request'])


class VerifyEmailSerializer(serializers.Serializer):
    code = serializers.UUIDField()
    csrf = serializers.UUIDField()

    def validate_code(self, value):
        return is_verification_code_valid(value)

    def validate_csrf(self, value):
        return is_csrf_valid(value, self.context['request'])
