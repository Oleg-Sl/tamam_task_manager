
from django.db import models
from django.utils import timezone


class TaskType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название задачи')
    description = models.TextField(verbose_name='Описание задачи')
    handler_path = models.CharField(max_length=255, verbose_name='Путь к обработчику')
    timeout = models.IntegerField(verbose_name='Максимальное времы выполнения', null=True, blank=True)

    class Meta:
        verbose_name = 'Тип задачи'
        verbose_name_plural = 'Типы задач'

    def __str__(self) -> str:
        return  self.name

class Task(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Ожидает выполнения'
        IN_PROGRESS = 'IN_PROGRESS', 'Вполняется'
        COMPLETED = 'COMPLETED', 'Завершена'

    class Outcome(models.TextChoices):
        SUCCESS = 'SUCCESS', 'Успешно'
        FAILED = 'FAILED', 'Провалено'

    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, db_index=True)
    input_data = models.JSONField(default=dict, blank=True)

    arrival_date = models.DateTimeField(default=timezone.now)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    outcome = models.CharField(
        max_length=16,
        choices=Outcome.choices,
        blank=True,
        null=True,
    )
    result_data = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ('-arrival_date',)

    def __str__(self) -> str:
        return f'{self.task_type.name} -  ({self.arrival_date})'
