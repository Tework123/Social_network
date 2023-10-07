from django.urls import path

from tasks.views import CreatePostView, PostEditView, DigitalAPiView, RedisTestView

urlpatterns = [

    path('', CreatePostView.as_view()),
    path('<int:pk>', PostEditView.as_view()),
    path('number/', DigitalAPiView.as_view()),
    path('test/', RedisTestView.as_view()),

]
