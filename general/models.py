import uuid
from django.db import models

# Базовая модель
class General(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_flg = models.BooleanField(default=False)

    class Meta:
        abstract = True

# Организация
class Organization(General):
    name = models.CharField(max_length=250, verbose_name='Название')
    description = models.CharField(max_length=250, verbose_name='Краткая информация')

    def __repr__(self) -> str:
        return f'{self.id}'

    def __str__(self) -> str:
        return f'{self.name} {self.id}'

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'