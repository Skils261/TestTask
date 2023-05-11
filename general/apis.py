from rest_framework.views import APIView
from accounts.utils import get_paginated_response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser
from rest_framework import(
    serializers,
    status,
)
from .selectors import(
    organization_get,
    organization_list,
)
from .services import(
    organization_create,
    organization_delete,
    organization_update,
)
from .models import Organization


class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = CustomUser
            fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'photo',)


# API просмотра организации по ID
class OrganizationDetailApi(APIView):
    permission_classes = (IsAuthenticated,)
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Organization
            fields = "__all__"
            depth = 1

    def get(self, request, id):
        organization = organization_get(id=id)
        serializer = self.OutputSerializer(organization)
        return Response(serializer.data)
    

# API просмотра списка всех не удаленных организаций
class OrganizationListApi(APIView):
    permission_classes = (IsAuthenticated,)
    class Pagination(LimitOffsetPagination):
        default_limit = 100

    class FilterSerializer(serializers.Serializer):
        id = serializers.CharField(required=False)
        
    class OutputSerializer(serializers.ModelSerializer):
        users = UserSerializer(source='user_organization', many=True)
        class Meta:
            model = Organization
            fields = ('name', 'description', 'users')

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        
        organization = organization_list(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=organization,
            request=request,
            view=self
        )
    

# API создания новой организации
class OrganizationCreateApi(APIView):
    permission_classes = (IsAuthenticated,)
    class InputOrganizationCreateSerializer(serializers.Serializer):
        name = serializers.CharField()
        description = serializers.CharField()
        
    @swagger_auto_schema(
        operation_id='OrganizationCreate',
        request_body=InputOrganizationCreateSerializer,
        responses={
            '201': '',
        })

    def post(self, request):
        serializer = self.InputOrganizationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization_create(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)


# API редактирования организации по ID
class OrganizationUpdateApi(APIView):
    permission_classes = (IsAuthenticated,)
    class InputOrganizationUpdateSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        description = serializers.CharField(required=False)
        
    @swagger_auto_schema(
        operation_id='OrganizationUpdate',
        request_body=InputOrganizationUpdateSerializer,
        responses={
            '200': '',
        })

    def post(self, request, id):
        serializer = self.InputOrganizationUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization_update(id=id, **serializer.validated_data)
        return Response(status=status.HTTP_200_OK)
    

# API удаления организации, из БД данные не удаляются
# происходит update deleted_flg на True
class OrganizationDeleteApi(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request, id):
        organization_delete(id=id)
        return Response(status=status.HTTP_200_OK)