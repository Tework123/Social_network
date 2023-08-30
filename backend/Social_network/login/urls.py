from django.urls import path

from login.views import ProfileList

urlpatterns = [

    path('', ProfileList.as_view())
]
