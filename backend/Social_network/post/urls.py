from django.urls import path

from post.views import CreatePostView, PostEditView

urlpatterns = [

    path('', CreatePostView.as_view()),
    path('<int:pk>', PostEditView.as_view()),

]
