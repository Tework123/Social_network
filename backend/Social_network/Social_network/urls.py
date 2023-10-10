from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

v1_urls = [
    path('login/', include('login.api.v1.urls')),
    path('account/', include('account.api.v1.urls')),
    path('album/', include('album.api.v1.urls')),
    path('chat/', include('chat.api.v1.urls')),
    path('community/', include('community.api.v1.urls')),
    path('post/', include('post.api.v1.urls')),

    # celery
    path('tasks/', include('tasks.api.v1.urls')),

]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("v1/", include((v1_urls, "v1"), namespace="v1")),

]

# swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Social network doc",
        default_version='v0.2.0',
        description="Api for social network",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # for my api change this url
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

# static
urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

# handler404 = pageNotFound
