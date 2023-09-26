from django.urls import path

from tasks.views import run_task, get_status

urlpatterns = [

    path("", run_task, name="run_task"),
    path("<task_id>/", get_status, name="get_status"),

]
