from django.urls import path, re_path

from login.views import ProfileList, CreateUserView, AuthUserView, activate, LogoutUserView, ResetPasswordSendEmail, \
    ResetPasswordCreatePassword, RegisterUserTryView, DeleteUserView

urlpatterns = [

    path('', ProfileList.as_view()),
    # регистрация
    path('register/', CreateUserView.as_view()),

    # повторная отправка для подтверждения аккаунта
    path('register_try/', RegisterUserTryView.as_view()),

    # получение ссылки для подтверждения аккаунта
    path('activate/<uidb64>/<token>/', activate, name='activate'),

    # авторизация
    path('auth/', AuthUserView.as_view()),

    # функционал для сброса пароля
    path('reset_password/',
         ResetPasswordSendEmail.as_view()),

    # получение ссылки для сброса пароля
    path('reset_password/<uidb64>/<token>/', ResetPasswordCreatePassword.as_view(), name='reset_password'),

    # выход из аккаунта
    path('logout/', LogoutUserView.as_view()),

    # удаление аккаунта
    path('delete/', DeleteUserView.as_view()),

]
