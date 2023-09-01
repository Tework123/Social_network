from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/login/', include('login.urls')),

    # авторизация
    path('api/v1/auth/', include('rest_framework.urls')),

    # # регистрация
    # path('api/v1//', include('register.urls')),

    path("__debug__/", include("debug_toolbar.urls")),

]

