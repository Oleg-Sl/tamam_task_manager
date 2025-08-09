from django.http import JsonResponse
from django.db import models

from users.models import UserToken
from tasks.models import Task, TaskType


def recalculate_product_calculations(request):
    token = request.GET.get('token', None)
    task_type_name = request.GET.get('task_type', None)

    try:
        user = UserToken.objects.get(token=token)
    except UserToken.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=401)

    try:
        task_type = TaskType.objects.get(name=task_type_name)
    except TaskType.DoesNotExist:
        return JsonResponse({'error': 'Invalid task_type'}, status=404)

    task_in_pending = Task.objects.filter(
        task_type=task_type
    ).filter(
        models.Q(status=Task.Status.PENDING) | models.Q(status=Task.Status.IN_PROGRESS)
    ).filter(
        outcome__isnull=True
    )

    if task_in_pending.exists():
        return JsonResponse({'error': 'Task already pending'}, status=409)

    task = Task.objects.create(task_type=task_type)

    return JsonResponse({'task': task.pk, 'task_type': task_type.name}, status=200)
