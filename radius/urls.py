from django.contrib.auth.decorators import login_required
from django.urls import path
from system.decorators import group_required

from .views import *

app_name = 'radius'
urlpatterns = [
    path('list/', group_required('Admin')(RadiusIndex.as_view()), name='list_radius'),
    path('add/', group_required('Admin')(AddRadius.as_view()), name='insert_radius'),
    path('radius_check_mail/', group_required('Admin')(radius_check_mail), name='radius_check_mail'),
    path('edit/<str:pk>/', group_required('Admin')(RadiusViewDate.as_view()), name='radius_edit_user'),
    path('delete/', group_required('Admin')(delete_users_radius), name='delete_users_radius'),
    path('change_passwd/', group_required('Admin')(PassRadius.as_view()), name='radius_change_passwd'),
    path('save/', group_required('Admin')(EditRadius.as_view()), name='radius_save_edit_user'),
]