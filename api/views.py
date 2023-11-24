
from rest_framework.viewsets import ModelViewSet 
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)
from django.conf import settings
from .serializers import *
import requests
from django.contrib.auth import get_user_model
UserModel = get_user_model()




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

    model = 'gpt-3.5-turbo'
    endpoint = 'https://api.openai.com/v1/chat/completions'
    headers = {'Authorization': f'Bearer {settings.OPENAI_API_KEY}'}

    queryset = UserModel.objects.order_by('-id')
    serializer_class = ChatMessageSerializer

    def get_completion(self, messages):
        data = dict(model=self.model, messages=messages)
        res = requests.post(url=self.endpoint, headers=self.headers, json=data)
        if hasattr(res, 'json'):
            print(res.json())
            return res['choices'][0]['message']
        print(res)
    

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            messages = user.chat_logs['messages']
            messages.append({'role':'user', 'content':serializer.validated_data['question']})
            messages.append(self.get_completion(messages))
            user.save()
            return Response(dict(response=messages[-1]['content']), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
