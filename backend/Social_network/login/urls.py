from django.urls import path, re_path

from login.views import ProfileList, CreateUserView, AuthUserView, activate, LogoutUserView, send_token_to_email

urlpatterns = [

    path('', ProfileList.as_view()),
    path('register/', CreateUserView.as_view()),
    # path('/', CreateUserView.as_view()),

    # авторизация
    path('auth/', AuthUserView.as_view()),

    # выход из аккаунта
    path('logout/', LogoutUserView.as_view()),

    # получение ссылки с токеном для подтверждения аккаунта
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            activate),

    # повторная отправка ссылки
    path('send_token_to_email/',
         send_token_to_email),

    # нужна еще ссылка с токеном для сброса пароля

]
