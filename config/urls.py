"""blogic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def app_version(request):
    return Response(settings.VERSIONS)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include('apps.api.v1.urls')),
    path('api/versions/', app_version, name='version')
]


if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    from rest_framework import permissions

    schema_view = get_schema_view(
        openapi.Info(
            title="Blogic Backend",
            default_version='v1',
            description="Prefix: /api/v1/"
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
        urlconf='apps.api.v1.urls',
    )

    urlpatterns += [
        path('api/root/', schema_view.with_ui('swagger',
                                              cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc',
                                           cache_timeout=0), name='schema-redoc'),
        path('', RedirectView.as_view(url='/api/root/', permanent=False)),
        path('__debug__/', include(debug_toolbar.urls)),
    ] + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    ) + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
