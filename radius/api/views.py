from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from radius.models import Users
from .serializers import UsersSerializer
from .pagination import UsersPagination

class UsersVS(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Users.objects.all().order_by('name', 'email')
    serializer_class = UsersSerializer
    pagination_class = UsersPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email', 'description', 'group__group_name']