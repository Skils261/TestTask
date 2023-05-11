from .models import(
    CustomUser,
)
        

# Функция создания нового пользователя        
def user_create(email: str,
                password: str,
                first_name: str,
                last_name: str,
                phone: str,
                is_active: bool = True,
                photo: str = None,
                organizations: str = None,
                ) -> CustomUser:
    
    obj = CustomUser(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        photo=photo,
        is_active=is_active,
    )
    obj.save()
    if organizations is not None:
        for organization in organizations:
            obj.organization.add(organization.get('organization').get('id'))
    return obj


# Функция редактирования пользователя
def user_update(id: str,
                email: str,
                first_name: str,
                last_name: str,
                phone: str,
                photo: str = None,
                organizations: str = None,
                ) -> None:
    kwargs = dict(locals())
    update_fields = {k: v for k,
                     v in kwargs.items() if v is not None and k != 'id'}
    CustomUser.objects.filter(id=id).update(**update_fields)
    if organizations is not None:
        for organization in organizations:
            CustomUser.objects.get(id=id).organization.add(organization.get('organization').get('id'))
    return None


# Функция удаления пользователя
def user_delete(id: str) -> None:
    CustomUser.objects.filter(id=id).update(is_active=False)
    return None


# Функция удаления организаций пользователя
def user_organizations_delete(*, id, organizations) -> None:
    for organization in organizations:
        CustomUser.objects.get(id=id).organization.remove(organization.get('organization').get('id'))
    return None