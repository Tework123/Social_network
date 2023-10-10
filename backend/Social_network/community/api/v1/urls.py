from django.urls import path

from community.api.v1.views import GetCommunities

urlpatterns = [

    path('', GetCommunities.as_view()),

]
