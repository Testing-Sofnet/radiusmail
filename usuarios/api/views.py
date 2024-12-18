from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from usuarios.models import Users
from system.models import UserProfile
from .serializers import UsuarioSerializer
from .pagination import UsersPagination
from django.db.models import Q

class UsuarioVS(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Users.objects.all().order_by('nombre', 'apellidos')
    serializer_class = UsuarioSerializer
    pagination_class = UsersPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'nombre', 'apellidos', 'ci', 'ocupacion__ocupacion_name', 'municipio__municipio_name']
    
    def get_queryset(self):        
        user_profile = UserProfile.objects.get(user=self.request.user.pk)
        if user_profile.user.groups.filter(Q(name='Representantes')):
            return super().get_queryset().filter(trabajo=user_profile.trabajo)
        elif user_profile.user.groups.filter(Q(name='Admin')):
            return super().get_queryset()