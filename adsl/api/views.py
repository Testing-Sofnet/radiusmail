from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from adsl.models import Enlace, Internet
from .serializers import EnlaceSerializer, InternetSerializer
from .pagination import EnlacePagination, InternetPagination

class EnlaceVS(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Enlace.objects.all().order_by('alias')
    serializer_class = EnlaceSerializer
    pagination_class = EnlacePagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['alias']


class InternetVS(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Internet.objects.all().order_by('adsl')
    serializer_class = InternetSerializer
    pagination_class = InternetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['ip']