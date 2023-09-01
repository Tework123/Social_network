from django.urls import path

from login.views import ProfileList, CreateUserView, AuthUserView, activate

urlpatterns = [

    path('', ProfileList.as_view()),
    path('register/', CreateUserView.as_view()),
    # path('/', CreateUserView.as_view()),

    # авторизация
    path('auth/', AuthUserView.as_view()),

    # получение ссылки с токеном для подтверждения аккаунта
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         activate, name='activate'),

    # нужна еще ссылка с токеном для сброса пароля

    # path('r', ProfileList.as_view()),

]
