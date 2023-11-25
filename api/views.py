
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, mixins, permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)
from django.conf import settings
from .serializers import *
from .models import *
import requests
from django.contrib.auth import get_user_model
UserModel = get_user_model()




class UsersViewSet(ModelViewSet):

    "API ViewSet to list out, create, retrieve, update and delete users"

    queryset = UserModel.objects.order_by('-id')
    serializer_class = UserSerializer

    @action(detail=True)
    def my_details(self, request, *args, **kwargs):
        ins = self.request.user 
        serializer = self.get_serializer(ins)
        return Response(serializer.data)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class LoginRefreshView(TokenRefreshView):
    serializer_class = LoginRefreshSerializer


class LogoutView(TokenBlacklistView):
    serializer_class = LogoutSerializer


class ChatSessionViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):

    "API Viewset to list out, create and retrieve the chat sessions belonging to the currently authenticated user"

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user).prefetch_related('user')
    
    def get_serializer_class(self):
        if self.action == 'respond_to_user':
            return ChatMessageSerializer
        return ChatSessionSerializer
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    model = 'gpt-3.5-turbo'
    endpoint = 'https://api.openai.com/v1/chat/completions'
    request_headers = {'Authorization': f'Bearer {settings.OPENAI_API_KEY}'}
    
    
    def get_completion(self, messages):
        data = dict(model=self.model, messages=messages)
        res = requests.post(url=self.endpoint, headers=self.request_headers, json=data)
        completion = None
        if hasattr(res, 'json'):
            if res.status_code==200:
                completion =  res.json()['choices'][0]['message']
            else:
                completion = res.json()
        return res.status_code, completion

    @action(detail=True)
    def respond_to_user(self, request, *args, **kwargs):
        session = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            messages = session.content['messages']
            messages.append({'role':'user', 'content':serializer.validated_data['question']})
            status_code, completion = self.get_completion(messages)
            if status_code != 200:
                return Response(completion or {'error':'Error processing request'}, status=status_code)
            messages.append(completion)
            session.content['messages'] = messages
            session.save()
            return Response(dict(response=messages[-1]['content']), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
