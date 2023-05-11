import django_filters
from .models import (
    CustomUser,
)


class BaseCustomUserFilter(django_filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = ['id',]


# Функция получения информации о конкретном пользователе
def user_get(*, id) -> CustomUser:
    return CustomUser.objects.get(id=id)

# Функция получения всех активных пользователей
def user_list(*, filters=None) -> CustomUser:
    filters = filters or {}
    qs = CustomUser.objects.filter(is_active=True)
    return BaseCustomUserFilter(filters, qs).qs