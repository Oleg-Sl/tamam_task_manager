from django.contrib import admin

from tasks.models import Task, TaskType


admin.site.register(Task)
admin.site.register(TaskType)
