from django.urls import path

from post.views import CreatePostView, PostEditView, DigitalAPiView

urlpatterns = [

    path('', CreatePostView.as_view()),
    path('<int:pk>', PostEditView.as_view()),
    path('number', DigitalAPiView.as_view()),

]
