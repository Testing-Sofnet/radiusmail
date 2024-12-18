from django.contrib.auth.decorators import login_required
from django.urls import path
from system.decorators import group_required

from .views import *

app_name = 'usuarios'
urlpatterns = [
    path('list/', group_required('Admin', 'Representantes')(ListUsers.as_view()), name='user_list'),
    path('check_ci/', group_required('Admin', 'Representantes')(check_ci), name='check_ci'),
    path('check_user/', group_required('Admin', 'Representantes')(check_user), name='check_user'),
    path('add/', group_required('Admin', 'Representantes')(AddUser.as_view()), name='insert_user'),
    path('edit/<str:pk>/', group_required('Admin', 'Representantes')(UserViewDate.as_view()), name='view_user'),
    path('delete/', group_required('Admin', 'Representantes')(delete_user), name='delete_user'),
    path('trasladar/', group_required('Admin')(TrasladoUsuario.as_view()), name='traslado_usuario'),
    path('change_passwd/', group_required('Admin', 'Representante')(PassChange.as_view()), name='user_change_passwd'),
    path('save/', group_required('Admin', 'Representante')(EditUser.as_view()), name='save_edit_user'),
    path('update/estado/', group_required('Admin', 'Representante')(update_estado_usuario), name='update_estado_usuario'),
    path('service/change/', group_required('Admin', 'Representantes')(ServiceChange.as_view()), name='service_change'),
    path('email/change/', group_required('Admin', 'Email')(EditMail.as_view()), name='email_change'),
    path('add_mac/', group_required('Admin', 'Wifi')(AddDevice.as_view()), name='insert_device'),
    path('wlan_check_mac/', group_required('Admin', 'Wifi')(wlan_check_mac), name='wlan_check_mac'),
    path('delete/mac/', group_required('Admin', 'Wifi')(delete_mac_wlan), name='delete_mac'),

]