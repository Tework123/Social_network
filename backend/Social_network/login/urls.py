from django.urls import path, re_path

from login.views import ProfileList, CreateUserView, AuthUserView, activate, LogoutUserView, \
    ProfilePhotoTest, ResetPasswordSendEmail, ResetPasswordCreatePassword

urlpatterns = [

    path('', ProfileList.as_view()),
    # регистрация
    path('register/', CreateUserView.as_view()),

    # получение ссылки для подтверждения аккаунта
    path('activate/<uidb64>/<token>/', activate, name='activate'),

    # авторизация
    path('auth/', AuthUserView.as_view()),

    # выход из аккаунта
    path('logout/', LogoutUserView.as_view()),

    # функционал для сброса пароля
    path('reset_password/',
         ResetPasswordSendEmail.as_view()),

    path('reset_password/<uidb64>/<token>/', ResetPasswordCreatePassword.as_view(), name='reset_password'),

    # path('reset_password_create/',
    #      ResetPasswordCreatePassword.as_view()),

    # повторная отправка для подтверждения аккаунта
    # path('activate_account/',
    #      send_token_to_email, name='send_token_to_email'),

    path('activate/<uidb64>/<token>/', activate, name='activate'),

    path('photos/', ProfilePhotoTest.as_view())

    # нужна еще ссылка с токеном для сброса пароля

]
