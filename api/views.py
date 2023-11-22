
from rest_framework.viewsets import ModelViewSet 
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

from .serializers import *

from django.contrib.auth import get_user_model
UserModel = get_user_model()

import openai
from django.conf import settings


class UsersViewSet(ModelViewSet):

    "API ViewSet to list out, create, retrieve, update and delete users"

    queryset = UserModel.objects.order_by('-id')
    serializer_class = UserSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class LoginRefreshView(TokenRefreshView):
    serializer_class = LoginRefreshSerializer


class LogoutView(TokenBlacklistView):
    serializer_class = LogoutSerializer


class ChatView(GenericAPIView):

    openai_model = 'gpt-3.5-turbo'
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    queryset = UserModel.objects.order_by('-id')
    serializer_class = ChatMessageSerializer

    def get_completion_response(self, messages):
        completion = self.client.chat.completions.create(
            model=self.openai_model, 
            messages=messages
        )
        return dict(completion.choices[0].message)

        # return {
        #     'role': 'assistant',
        #     'content': 'I am ChatGPT!'
        # }

    def post(self, request, *args, **kwargs):
        user = self.get_object()

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            question = serializer.validated_data['question']
            messages = user.chat_logs['messages']
            messages.append({'role':'user', 'content':question})

            completion = self.get_completion_response(messages)
            messages.append(completion)

            user.chat_logs['messages'] = messages
            user.save()

            return Response({
                'response': completion['content']
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
