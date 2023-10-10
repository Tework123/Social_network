from django.urls import path

from login.api.v1.views import (RegisterView, activate,
                                LogoutUserView, ResetPasswordSendEmailView,
                                ResetPasswordCreatePasswordView, RegisterTryView,
                                DeleteUserView, AuthView)

urlpatterns = [

    # регистрация
    path('register/', RegisterView.as_view()),

    # повторная отправка для подтверждения аккаунта
    path('register_try/', RegisterTryView.as_view()),

    # получение ссылки для подтверждения аккаунта
    path('activate/<uidb64>/<token>/', activate, name='activate'),

    # авторизация
    path('auth/', AuthView.as_view()),

    # функционал для сброса пароля
    path('reset_password/',
         ResetPasswordSendEmailView.as_view()),

    # получение ссылки для сброса пароля
    path('reset_password/<uidb64>/<token>/', ResetPasswordCreatePasswordView.as_view(),
         name='reset_password'),

    # выход из аккаунта
    path('logout/', LogoutUserView.as_view()),

    # удаление аккаунта
    path('delete/', DeleteUserView.as_view()),

]
