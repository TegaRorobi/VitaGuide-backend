
from django.urls import re_path 

from .aliases import *
from .views import *


urlpatterns = [

    re_path('^auth/login/?$', LoginView.as_view(), name='api-login'),
    re_path('^auth/login/refresh/?$', LoginRefreshView.as_view(), name='api-login-refresh'),
    re_path('^auth/logout/?$', LogoutView.as_view(), name='api-logout'),

    re_path('^users/all/?$', UsersViewSet.as_view(LIST), name='users-list'),
    re_path('^users/create/?$', UsersViewSet.as_view(CREATE), name='user-create'),

    re_path('^user/me/retrieve/?$', UsersViewSet.as_view(RETRIEVE), name='user-retrieve'),
    re_path('^user/me/update/?$', UsersViewSet.as_view(PARTIAL_UPDATE), name='user-update'),
    re_path('^user/me/delete/?$', UsersViewSet.as_view(DESTROY), name='user-delete'),

    re_path('^chat/sessions/all/?$', ChatSessionViewSet.as_view(LIST), name='chat-sessions-list'),
    re_path('^chat/session/create/?$', ChatSessionViewSet.as_view(CREATE), name='chat-session-create'),
    re_path('^chat/session/(?P<pk>\d+)/retrieve/?$', ChatSessionViewSet.as_view(RETRIEVE), name='chat-session-retrieve'),
    re_path('^chat/session/(?P<pk>\d+)/interact/?$', ChatSessionViewSet.as_view({'post':'respond_to_user'}), name='user-chat'),
    # re_path('^chat/(?P<pk>\d+)/retrieve/?$', ChatViewSet.as_view({'get':'retrieve_chat_log'}), name='chat-retrieve'),

]