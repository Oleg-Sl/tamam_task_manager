
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from tasks.models import Task


@receiver(pre_save, sender=Task)
def update_task_dates(sender, instance: Task, **kwargs):
    if instance.status == instance.Status.IN_PROGRESS and instance.start_date is None:
        instance.start_date = timezone.now()
    elif instance.status == instance.Status.COMPLETED and instance.end_date is None:
        instance.end_date = timezone.now()
