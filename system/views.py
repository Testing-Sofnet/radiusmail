import datetime
import json
from django.contrib.auth import forms, login, logout, authenticate
from django.core import paginator, serializers
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext, Context
from django.views import generic
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, DetailView
from django.contrib import messages
from django.conf import settings
from .models import *
from usuarios.models import Users
from adsl.models import Enlace

#from .forms import *







def get_client_ip(request):
    """Función auxiliar para obtener la IP del cliente de forma segura"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    return ip

class Login(View):
    form = forms.AuthenticationForm

    def get(self, request):
        context = {'form': self.form()}
        return render(request, 'login.html', context)

    def post(self, request):
        form = self.form(None, request.POST)
        context = {'form': form}
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            username = request.POST['username']
            password = request.POST['password']
            
            # Obtener IP de manera más segura
            ip_address = get_client_ip(request)
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    if user.is_superuser:
                        login(request, user)
                        msg = f'El usuario {user.first_name} {user.last_name} ({user.email}) entro al sistema'
                        Logs.objects.create(users=user, ip=ip_address, comentario=msg, msg_type=1)
                        return HttpResponse('1')
                    else:
                        try:
                            user_profile = UserProfile.objects.get(user=user.pk)
                            if user_profile.ip_address != ip_address:
                                msg_logs = f'Error del usuario {user.first_name} {user.last_name} ({user.email}) intentando entrar desde un ip no autorizado'
                                Logs.objects.create(users=user, ip=ip_address, comentario=msg_logs, msg_type=3)
                                return HttpResponse('4')
                            else:
                                login(request, user)
                                msg = f'El usuario {user.first_name} {user.last_name} ({user.email}) entro al sistema'
                                Logs.objects.create(users=user, ip=ip_address, comentario=msg, msg_type=1)
                                return HttpResponse('1')
                        except UserProfile.DoesNotExist:
                            return HttpResponse('2')
                else:
                    return HttpResponse('3')
            else:
                return HttpResponse('2')
        return render(request, 'login.html', context)


class Logout(View):
    def get(self, request):
        user = request.user
        # Usar la función auxiliar para obtener la IP
        ip_address = get_client_ip(request)

        msg_logs = f'El usuario {user.first_name} {user.last_name} ({user.email}) salio del sistema'
        
        # Usar create en lugar de instanciar y guardar
        Logs.objects.create(
            users=user,  # Usar users en lugar de users_id
            ip=ip_address,
            comentario=msg_logs,
            msg_type=2
        )
        
        logout(request)
        return redirect('login')


class Dashboard(View):
    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user.pk)
        
        if user_profile.user.groups.filter(Q(name='Representantes')):
            report_log = Logs.objects.filter(users=user_profile.user).order_by('-pk')[:7]
            report_users = Users.objects.filter(trabajo=user_profile.trabajo).order_by('-pk')[:7]
            
            type_logs = Logs.objects.filter(users=user.user_profile.user).values('msg_type').annotate(Count('msg_type'))
            report_type_logs = []
            for type in type_logs:
                report_type_logs.append({'logs': type})
            
            type_service = Users.objects.filter(trabajo=user_profile.trabajo).values('sldservice__service_name').annotate(Count('sldservice'))
            report_type_service = []
            for service in type_service:
                report_type_service.append({'services': service})
        else:
            report_log = Logs.objects.all().order_by('-pk')[:7]
            report_users = Users.objects.all().order_by('-pk')[:7]
            
            type_logs = Logs.objects.all().values('msg_type').annotate(Count('msg_type'))
            report_type_logs = []
            for type in type_logs:
                report_type_logs.append({'logs': type})
                
            
            type_service = Users.objects.all().values('sldservice__service_name').annotate(Count('sldservice'))
            report_type_service = []
            for service in type_service:
                report_type_service.append({'services': service})
            
            


        context_data = {
            'title': 'Dashboard',
            'report_log': report_log,
            'report_users': report_users,
            'report_type_logs': report_type_logs,
            'report_type_service': report_type_service,
        }
        return render(request, 'dashboard.html', context_data)


class Profile(View):
    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user.pk)
        my_logs = Logs.objects.filter(users=user).order_by('-pk')[:10]
        total_users = ''
        adsl = ''
        if user_profile.user.groups.filter(Q(name='Representantes')):
            total_users = Users.objects.filter(trabajo=user_profile.trabajo).count()
            adsl = Enlace.objects.filter(trabajo=user_profile.trabajo)

        context_data = {
            'title': 'Perfil',
            'my_logs': my_logs,
            'user_profile': user_profile,
            'total_users': total_users,
            'adsl': adsl,
        }
        return render(request, 'profile.html', context_data)


class ListLogs(View):
    def get(self, request):


        context_data = {
            'title': 'Logs del sistema',
        }
        return render(request, 'logs.html', context_data)


class ChangePasswd(View):
    def post(self, request):
        user = request.user
        ip_address = request.META['REMOTE_ADDR']
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            passwd = request.POST['passwd']
            try:
                user.set_password(passwd)
                user.save()
                #messages.success(request, "Clave actualizada correctamente")

                msg_logs = 'El usuario %s %s (%s) modifico su password' % (user.first_name, user.last_name, user.email)
                Logs(users=user, ip=ip_address, comentario=msg_logs, msg_type=105).save()

                msg = {'status': True, 'msg': 'Password modificado con exito'}
                return HttpResponse(json.dumps(msg))
            except:
                msg = {'status': False, 'msg': 'Error al modificar el password'}
                return HttpResponse(json.dumps(msg))

@csrf_exempt
def system_get_unidad(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        municipio = Municipio.objects.get(pk=int(request.POST['id_municipio']))
        unidad = Trabajo.objects.filter(municipio=municipio)
        data = serializers.serialize("json", unidad, fields=('id', 'trabajo_name'))

    return HttpResponse(data, content_type="application/javascript")