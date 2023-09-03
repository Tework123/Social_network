from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/login/', include('login.urls')),

    # авторизация
    path('api/v1/auth/', include('rest_framework.urls')),

    # # регистрация
    # path('api/v1//', include('register.urls')),

    path("__debug__/", include("debug_toolbar.urls")),

]

urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
# handler404 = pageNotFound
