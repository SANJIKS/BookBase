from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
        openapi.Info(
            title="Books",
            default_version='v1',
            description="API for Books",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="contact@snippets.local"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=[permissions.IsAdminUser],
    )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger',
        cache_timeout=0), name='schema-swagger-ui'),
    path('users/', include('users.urls')),
    path('books/', include('books.urls'))
]                                                                                                                                           


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)