import json
import importlib

from django.core.management.base import BaseCommand, CommandError
from django.utils.module_loading import import_string
from django.conf import settings
from django.utils import timezone

from tasks import recalculate_product_calculation
from tasks.models import Task


class Command(BaseCommand):
    help = "Recalculation of product calculations"

    def handle(self, *args, **options):
        tasks = Task.objects.filter(status=Task.Status.PENDING)
        for task in tasks:
            handler_path = task.task_type.handler_path
            task.status = Task.Status.IN_PROGRESS
            task.start_date = timezone.now()
            task.save()
            try:
                handler_path = task.task_type.handler_path
                # handler_path = 'tasks.recalculate_product_calculation.main.recalculate'
                handler = import_string(handler_path)
                result = handler(task.input_data) if task.input_data else handler()
                task.result_data = json.dumps(result)
                task.outcome = Task.Outcome.SUCCESS
            except Exception as err:
                task.result_data = str(err)
                task.outcome = Task.Outcome.FAILED
            finally:
                task.status = Task.Status.COMPLETED
                task.end_date = timezone.now()
                task.save()
