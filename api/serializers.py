
from rest_framework import serializers

from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenBlacklistSerializer
)

from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = '__all__'

    def create(self, validated_data):
        clear_password = validated_data['password']
        validated_data['password'] = make_password(clear_password)
        validated_data.setdefault('is_active', True)
        return super().create(validated_data)


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        return {
            **super().validate(attrs), **{
                'id': self.user.id,
                'email': self.user.email, 
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
            }
        }


class LoginRefreshSerializer(TokenRefreshSerializer):
    pass


class LogoutSerializer(TokenBlacklistSerializer):
    pass


class ChatMessageSerializer(serializers.Serializer):
    
    question = serializers.CharField()