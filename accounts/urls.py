from django.urls import path, include

from .apis import (
    UserDetailApi,
    UserListApi,
    UserCreateApi,
    UserUpdateApi,
    UserOrganizationDeleteApi,
    UserDeleteApi,
)

custom_user_patterns = [
    path('', UserListApi.as_view(), name='list'),
    path('<str:id>/detail', UserDetailApi.as_view(), name='deteil'),
    path('create', UserCreateApi.as_view(), name='create'),
    path('update', UserUpdateApi.as_view(), name='update'),
    path('<str:id>/delete', UserDeleteApi.as_view(), name='delete'),
    path('<str:id>/delete_organization', UserOrganizationDeleteApi.as_view(), name='delete_organizaton'),
]


urlpatterns = [
    path('users/', include((custom_user_patterns, 'user'))),
]