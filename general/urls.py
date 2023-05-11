from django.urls import path, include
from .apis import (
    OrganizationCreateApi,
    OrganizationDeleteApi,
    OrganizationDetailApi,
    OrganizationListApi,
    OrganizationUpdateApi,
)

organization_patterns = [
    path('', OrganizationListApi.as_view(), name='list'),
    path('<str:id>/detail', OrganizationDetailApi.as_view(), name='deteil'),
    path('create', OrganizationCreateApi.as_view(), name='create'),
    path('create', OrganizationUpdateApi.as_view(), name='update'),
    path('<str:id>/delete', OrganizationDeleteApi.as_view(), name='delete'),
]


urlpatterns = [
    path('organization/', include((organization_patterns, 'organization'))),
]