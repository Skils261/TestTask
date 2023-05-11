from .models import(
    Organization,
)
        

# Функция создания новой организации
def organization_create(name: str,
                        description: str,
                       ) -> Organization:
    
    obj = Organization(
        name=name,
        description=description,
    )
    obj.save()
    return obj


# Функция редактирования организации
def organization_update(id: str,
                        name: str = None,
                        description: str = None,
                        ) -> None:
    kwargs = dict(locals())
    update_fields = {k: v for k,
                     v in kwargs.items() if v is not None and k != 'id'}
    Organization.objects.filter(id=id).update(**update_fields)
    return None


# Функция удаления организации
def organization_delete(id: str) -> None:
    Organization.objects.filter(id=id).update(deleted_flg=True)
    return None