from django.contrib.auth.decorators import login_required
from django.urls import path
from .decorators import group_required

from .views import *

app_name = 'system'
urlpatterns = [
    path('change_passwd/', login_required(ChangePasswd.as_view(), login_url='login'), name='passwd'),
    path('logs/', group_required('Admin')(ListLogs.as_view()), name='list_logs'),
    #path('check_mail/', group_required('Admin')(system_check_mail), name='check_mail'),
    path('get_unidad/', login_required(system_get_unidad, login_url='login'), name='getUnidad'),
]