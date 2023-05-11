from rest_framework.views import APIView
from .models import CustomUser
from .utils import get_paginated_response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import(
    serializers,
    status,
)
from .selectors import(
    user_get,
    user_list,
)
from .services import(
    user_create,
    user_update,
    user_delete,
    user_organizations_delete,
)
from django.views.generic import UpdateView
from rest_framework.permissions import IsAuthenticated


class InputOrganizationSerializer(serializers.Serializer):
    id = serializers.CharField()
        
        
class CreateUpdateOrganizationSerializer(serializers.Serializer):
    organization = InputOrganizationSerializer(required=False)


# API для получения информации по конкретному пользователю
class UserDetailApi(APIView):
    permission_classes = (IsAuthenticated,)
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = CustomUser
            exclude = ('password',)
            depth = 1

    def get(self, request, id):
        user = user_get(id=id)
        serializer = self.OutputSerializer(user)
        return Response(serializer.data)
    

# API для получения списка всех активных пользователей  
class UserListApi(APIView):
    permission_classes = (IsAuthenticated,)
    class Pagination(LimitOffsetPagination):
        default_limit = 100

    class FilterSerializer(serializers.Serializer):
        id = serializers.CharField(required=False)
        
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = CustomUser
            exclude = ('password',)
            depth = 1

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        
        user = user_list(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=user,
            request=request,
            view=self
        )
        

# API создания нового пользователя
class UserCreateApi(APIView):
    permission_classes = (IsAuthenticated,)
    class InputUserCreateSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        phone = serializers.CharField()
        photo = serializers.ImageField(required=False)
        organizations = CreateUpdateOrganizationSerializer(required=False, many=True)
        is_active = serializers.BooleanField(default=True)

    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()

    @swagger_auto_schema(
        operation_id='UserCreate',
        request_body=InputUserCreateSerializer,
        responses={
            '201': '',
        })

    def post(self, request):
        serializer = self.InputUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = user_create(**serializer.validated_data)
        return Response(self.OutputSerializer(user).data)
    

# API редактирования пользователя
class UserUpdateApi(UpdateView):
    permission_classes = (IsAuthenticated,)
    class InputUserUpdateSerializer(serializers.Serializer):
        email = serializers.EmailField(required=False)
        first_name = serializers.CharField(required=False)
        last_name = serializers.CharField(required=False)
        phone = serializers.CharField(required=False)
        photo = serializers.ImageField(required=False)
        organizations = CreateUpdateOrganizationSerializer(required=False, many=True)
        
    @swagger_auto_schema(
        operation_id='UserUpdateSerializer',
        request_body=InputUserUpdateSerializer,
        responses={
            '200': '',
        })

    def post(self, request, id):
        serializer = self.InputUserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_update(id=id, **serializer.validated_data)
        return Response(status=status.HTTP_200_OK)
    

# API для удаления пользователя, пользователь не удаляется из БД
# При удалении пользователя происходит update флага is_active на False
class UserDeleteApi(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request, id):
        user_delete(id=id)
        return Response(status=status.HTTP_200_OK)
    

# API для удаления прикрепленных организаций к пользователю
class UserOrganizationDeleteApi(APIView):
    permission_classes = (IsAuthenticated,)
    class InputOrganizationDeleteSerializer(serializers.Serializer):
        organizations = CreateUpdateOrganizationSerializer(required=False, many=True)
        
    @swagger_auto_schema(
        operation_id='UserOrganizationDelete',
        request_body=InputOrganizationDeleteSerializer,
        responses={
            '200': '',
        })

    def delete(self, request, id):
        serializer = self.InputOrganizationDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_organizations_delete(id=id, **serializer.validated_data)
        return Response(status=status.HTTP_200_OK)