
from rest_framework import serializers

from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenBlacklistSerializer
)
from .models import ChatSession
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    chat_sessions = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    class Meta:
        model = UserModel
        fields = '__all__'
        extra_kwargs = {
            'is_active': {'read_only':True},
            'is_staff': {'read_only':True},
            'date_joined': {'read_only':True},
            'is_superuser': {'read_only':True},
            'chat_log': {'read_only':True},
        }

    def create(self, validated_data):
        clear_password = validated_data['password']
        validated_data['password'] = make_password(clear_password)
        validated_data.setdefault('is_active', True)
        return super().create(validated_data)


class ChatSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatSession
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only':True}
        }

    def to_representation(self, instance):
        ret =  super().to_representation(instance)
        a = ret['content']['messages']
        ret['content']['messages'] = a[1:]
        return ret


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