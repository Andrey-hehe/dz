from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    input_data = models.CharField('входные данные', max_length=200, unique=True)
    output_data = models.CharField('выходные данные', max_length=200)
    
    def __str__(self):
        return f"Task {self.id}: {self.input_data[:50]}..."

class Request(models.Model):
    """
    Модель для хранения запросов пользователей к задачам
    """
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE,
        verbose_name='Задача',
        related_name='requests'  # позволяет обращаться task.requests.all()
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='requests'  # позволяет обращаться user.requests.all()
    )
    
    created_at = models.DateTimeField(
        'Время создания',
        default=timezone.now,  # автоматически устанавливает текущее время UTC
        db_index=True  # индекс для ускорения поиска по дате
    )
    
    # Дополнительные поля, если нужно:
    # status = models.CharField(max_length=20, default='pending', choices=[...])
    # execution_time = models.DurationField(null=True, blank=True)
    # input_params = models.JSONField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'
        ordering = ['-created_at']  # сортировка по убыванию даты (новые сначала)
        indexes = [
            models.Index(fields=['user', 'created_at']),  # составной индекс
            models.Index(fields=['task', 'created_at']),   # еще один составной индекс
        ]
    
    def __str__(self):
        return f"Request {self.id}: {self.user.username} -> Task {self.task.id} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}"