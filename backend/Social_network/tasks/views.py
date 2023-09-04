# from django.http import JsonResponse
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from tasks.tasks import create_task
#
#
# @csrf_exempt
# def run_task(request):
#     if request.POST:
#         task_type = request.POST.get("type")
#         task = create_task.delay(int(task_type))
#
#         return JsonResponse({"task_id": task.id}, status=202)