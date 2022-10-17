from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Event(models.Model):
    title = models.CharField(
        max_length=100, verbose_name='Título'
    )
    description = models.TextField(
        blank=True, null=True, verbose_name='Descrição'
    )
    local = models.TextField(
        blank=True, null=True, verbose_name='Local'
    )
    date = models.DateTimeField(
        verbose_name='Data do evento'
    )
    creation_date = models.DateTimeField(
        auto_now=True, verbose_name='Data da criação'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Usuário'
    )

    class Meta:
        db_table = 'evento'

    def __str__(self):
        return self.title

    def get_event_input_date(self):
        return self.date.strftime('%Y-%m-%dT%H:%M')

    def islate(self):
        return self.date < timezone.now()

    def isimminent(self):
        now = timezone.now()
        return now < self.date < now + timedelta(hours=1)
