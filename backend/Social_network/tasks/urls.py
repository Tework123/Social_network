from django.urls import path

from tasks.views import run_task

urlpatterns = [

    path("", run_task, name="run_task"),
]
