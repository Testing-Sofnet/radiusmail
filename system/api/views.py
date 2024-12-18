from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from system.models import Logs
from .serializers import LogsSerializer
from .pagination import LogsPagination

class LogsVS(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Logs.objects.all().order_by('-access_date', '-id')
    serializer_class = LogsSerializer
    pagination_class = LogsPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['users__username', 'comentario', 'access_date', 'ip']