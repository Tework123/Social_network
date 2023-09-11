from django.urls import path

from community.views import GetCommunities

urlpatterns = [

    path('', GetCommunities.as_view()),

]
