import django_filters
from .models import (
    Organization,
)


class BaseOrganizationFilter(django_filters.FilterSet):
    class Meta:
        model = Organization
        fields = ['id',]


# Функция получения информации о конкретной оргиназации
def organization_get(*, id) -> Organization:
    return Organization.objects.get(id=id)


# Функция получения списка всех не удаленных оргиназаций
def organization_list(*, filters=None) -> Organization:
    filters = filters or {}
    qs = Organization.objects.filter(deleted_flg=False)
    return BaseOrganizationFilter(filters, qs).qs