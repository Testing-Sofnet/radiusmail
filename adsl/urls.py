from django.contrib.auth.decorators import login_required
from django.urls import path
from system.decorators import group_required

from .views import *

app_name = 'enlaces'
urlpatterns = [
    path('', group_required('Enlaces', 'Admin')(AdslIndex.as_view()), name='list_adsl'),
    path('check_ipwan/', group_required('Enlaces', 'Admin')(adsl_check_ipwan), name='check_ipwan'),
    path('check_iplan/', group_required('Enlaces', 'Admin')(adsl_check_iplan), name='check_iplan'),
    path('check_ipinternet/', group_required('Admin')(adsl_check_ipinternet), name='check_ipinternet'),
    path('add/', group_required('Admin')(AddEnlace.as_view()), name='insert_enlace'),
    path('delete/', group_required('Admin')(delete_enlace), name='delete_enlaces'),
    path('edit/<str:pk>/', group_required('Enlaces', 'Admin')(EnlaceViewDate.as_view()), name='enlace_edit'),
    path('trasladar/', group_required('Admin')(TrasladoEnlace.as_view()), name='traslado_enlace'),
    path('change_ip_lan/', group_required('Admin')(CambioBloqueIP.as_view()), name='cambio_ip_lan'),
    path('change_ab/', group_required('Admin')(CambioAB.as_view()), name='cambio_ab'),
    path('change_tec/', group_required('Admin')(CambioTec.as_view()), name='cambio_tec'),
    path('change_ip_internet/', group_required('Admin')(CambioIPInternet.as_view()), name='cambio_ip_internet'),
    path('change_permiso_internet/', group_required('Admin')(ActualizarPermiso.as_view()), name='actualizar_permiso'),
    path('assign_internet/', group_required('Admin')(AsignarInternet.as_view()), name='asignar_internet'),
    path('route/', group_required('Admin')(route_enlace), name='route_enlace'),
    path('internet/', group_required('Enlaces', 'Admin')(InternetIndex.as_view()), name='list_internet'),
]