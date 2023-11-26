
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status, mixins, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from django.conf import settings
from .serializers import *
from .models import *
import requests

UserModel = get_user_model()




class UsersViewSet(ModelViewSet):

    "API ViewSet to list out, create, retrieve, update and delete users"

    queryset = UserModel.objects.order_by('-id')
    serializer_class = UserSerializer
    def get_permissions(self):
        if self.action in ('create', 'list'):
            return [permissions.AllowAny()]
        return  [permissions.IsAuthenticated()]

    def get_object(self):
        return self.request.user
    

    @swagger_auto_schema(
        operation_summary='List out all users',
        operation_description='This endpoint returns a paginated response of '
        'all users stored in the database, with all necessary fields.'
    )
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)
    

    @swagger_auto_schema(
        operation_summary='Create a new user',
        operation_description='This endpoint accepts the common parameters of a user (full_name, email, password), '
        'saves the user to the database and returns the created user.'
    )
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)
    

    @swagger_auto_schema(
        operation_summary='Retrieve the details of the currently authenticated user',
        operation_description='This endpoint doesn\'t accept any parameters, and simply '
        'returns the details of the currently authenticated user'
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)
    
    
    @swagger_auto_schema(
        operation_summary='Update some details of the currently authenticated user',
        operation_description='This endpoint updates the currently authenticated user, with only'
        'the fields sent in the request body.'
    )
    def partial_update(self, *args, **kwargs):
        return super().partial_update(*args, **kwargs)
    

    @swagger_auto_schema(
        operation_summary='Delete the currently authenticated user ⚠⚠',
        operation_description='This endpoint deletes the currently authenticated user\'s account. '
        'This is NOT REVERSIBLE.'
    )
    def destroy(self, *args, **kwargs):
        return super().destroy(*args, **kwargs)

    




class LoginView(TokenObtainPairView):

    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_summary='Get a user\'s JWT refresh and access tokens.',
        operation_description='Takes a set of user credentials (email and password) and returns '
        'an access and refresh JSON web\ntoken pair to prove the authentication of those credentials.'
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class LoginRefreshView(TokenRefreshView):

    serializer_class = LoginRefreshSerializer

    @swagger_auto_schema(
        operation_summary='Refresh a user\'s JWT access token with a refresh token.',
        operation_description='Takes a user\'s refresh token and generates a new access token from it and returns it.'
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class LogoutView(TokenBlacklistView):

    serializer_class = LogoutSerializer

    @swagger_auto_schema(
        operation_summary='Invalidate a user\'s JWT refresh token',
        operation_description='Takes a user\'s refresh token and blacklists it, thereby invalidating it as a form of logout.'
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class ChatSessionViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):

    "API Viewset to list out, create and retrieve the chat sessions belonging to the currently authenticated user"

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user).prefetch_related('user')
    
    def get_serializer_class(self):
        if self.action == 'respond_to_user':
            return ChatMessageSerializer
        return ChatSessionSerializer
    
    @swagger_auto_schema(
        operation_summary="Get all of the currently authenticated user's chat sessions",
        operation_description="This endpoint returns a paginated response of all the chat sessions engaged by "
        "the currently authenticated user."
    )
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Retrieve the details of one of the currently authenticated user's chat sessions",
        operation_description="This endpoint accepts the id of one of the currently authenticated user's chat "
        "sessions, retrieves this session and then returns it."
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new chat session for the currently authenticated user",
        operation_description="This endpoint accepts an optional argument, 'title' (which defaults to 'New Session'), "
        "creates a new chat session for the currently authenticated user, and returns its details."
    )
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)
    
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
    @swagger_auto_schema(
        operation_summary="Enter a question and get a context-considered response from the chatbot",
        operation_description="This endpoint accepts the id of one of the currently authenticated user's chat sessions, "
        "and returns a response, taking into consideration all of the existing context from the session."
    )
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
