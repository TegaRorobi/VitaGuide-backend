"""
URL configuration for core project.
"""


from django.contrib import admin
from django.urls import path, re_path, include

from rest_framework.permissions import AllowAny
from django.conf.urls.static import static
from django.conf import settings

from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
    openapi.Info(
        title='Klusterthon Project API',
        default_version='v1',
        description='API Documentation for team 204\'s Klusterthon Hackathon project',
        contact=openapi.Contact(email='support@klusterthon204.com'),
        license=openapi.License(name='BSD License'),
    ),
    permission_classes=(AllowAny,),
    public=True
)


urlpatterns = [
    #admin
    re_path(f'^{settings.ADMIN_URL.strip()}/', admin.site.urls),

    # urlconfs
    path('api/', include('api.urls')),

    # swagger/redoc
    re_path('^api/swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(), name='schema-json'),
    re_path('^api/swagger/?$', schema_view.with_ui('swagger'), name='schema-swagger'),
    re_path('^api/redoc/?$', schema_view.with_ui('redoc'), name='schema-redoc'),
]