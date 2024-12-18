import datetime
import json
import requests
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
from .forms import UsersForm, TrasladarForm, DatosPersonalesForm, ServiceForm, DatosMailForm, DeviceForm
from system.models import Logs, UserProfile, Municipio


class ListUsers(View):
    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user.pk)
        uidnumberlist = list(Users.objects.all().values_list('uidNumber', flat=True))
        uidnumberlist.sort()
        if len(uidnumberlist) == 0:
            uidnumber = 10001
        else:
            uidnumber = uidnumberlist[-1] + 1        
        totaluser = ''
        if user_profile.user.groups.filter(Q(name='Representantes')):
            totaluser = Users.objects.filter(trabajo=user_profile.trabajo).count()


        context_data = {
            'title': 'Listado de usuarios',
            'totaluser': totaluser,
            'userform': UsersForm(),
            'user_profile': user_profile,
            'uidnumber': uidnumber,
        }
        return render(request, 'usuarios/users.html', context_data)


@csrf_exempt
def check_ci(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            Users.objects.get(ci=request.POST['ci'])
            msg = {'valid': False}
        except:
            msg = {'valid': True}

        return HttpResponse(json.dumps(msg))


@csrf_exempt
def check_user(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            Users.objects.get(email=request.POST['email'])
            msg = {'valid': False}
        except:
            msg = {'valid': True}

        return HttpResponse(json.dumps(msg))


class AddUser(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            user = request.user
            add = UsersForm(request.POST)
            if add.is_valid():
                name_municipio = list(Municipio.objects.filter(pk=request.POST['municipio']).values_list('municipio_name', flat=True))
                name_ocupacion = list(Ocupacion.objects.filter(pk=request.POST['ocupacion']).values_list('ocupacion_name', flat=True))
                name_service = []
                for x in request.POST.getlist('sldservice'):
                    name_service += Services.objects.filter(pk=x).values_list('service', flat=True)
                dataadd = {'nombre': request.POST['nombre'], 'apellidos': request.POST['apellidos'], 'ci': request.POST['ci'],  'quota': request.POST['quota'], 'tipo_cuenta': request.POST['tipo_cuenta'], 'municipio': name_municipio, 'ocupacion': name_ocupacion, 'uidNumber': request.POST['uidNumber'], 'email': request.POST['email'], 'sldservice': name_service, 'passwd': request.POST['passwd1']}
                apipost = requests.post(settings.API_URL + "mail/add/", data=dataadd)
                addrequest = apipost.json()
                if addrequest['status']:
                    add.save()
                    ip_address = request.META['REMOTE_ADDR']
                    msg_logs = 'El usuario %s %s (%s) creo la cuenta %s' % (
                    request.user.first_name, request.user.last_name, request.user.email, request.POST['email'])
                    Logs(users=request.user, ip=ip_address, comentario=msg_logs, msg_type=100).save()
                    messages.success(request, "Usuario creado correctamente")
                    msg = {'status': True, 'msg': 'Usuario creado sin error'}
                    return HttpResponse(json.dumps(msg))
                else:
                    msg = {'status': False, 'msg': 'Ocurrió un error en Ldap\n' + addrequest['error']['desc']}
                    return HttpResponse(json.dumps(msg))
            else:
                msg = {'status': False, 'msg': 'Formulario no valido'}
                return HttpResponse(json.dumps(msg))


class UserViewDate(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        munic = Municipio.objects.all().order_by('municipio_name')
        getuser = get_object_or_404(Users, pk=urlsafe_base64_decode(kwargs['pk']))
        service_list = Services.objects.filter(UsersService=getuser)
        totalmac = Device.objects.filter(user=getuser).count()
        context = {'title': getuser, 'getuser': getuser, 'totalmac': totalmac, 'service_list': service_list, 'munic': munic, 'deviceform': DeviceForm(),'trasladarform': TrasladarForm(instance=getuser), 'datospersonalesform': DatosPersonalesForm(instance=getuser), 'serviceform': ServiceForm(instance=getuser), 'datosmailform': DatosMailForm(instance=getuser)}
        return render(request, 'usuarios/user_edit.html', context)

@csrf_exempt
def delete_user(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        apipost = requests.delete(settings.API_URL + "mail/delete/" + request.POST['user'] + '/')
        addrequest = apipost.json()
        if addrequest['status']:
            ip_address = request.META['REMOTE_ADDR']
            msg_logs = 'El usuario %s %s (%s) borro la cuenta %s' % (
            request.user.first_name, request.user.last_name, request.user.email, request.POST['user'])
            Logs(users=request.user, ip=ip_address, comentario=msg_logs, msg_type=101).save()

            Users.objects.get(email=request.POST['user']).delete()
            messages.success(request, "Usuario eliminado correctamente")
            msg = {'status': True, 'msg': 'Usuario eliminado correctamente'}
            return HttpResponse(json.dumps(msg))
        else:
            msg = {'status': False, 'msg': 'Ocurrió un error en LDAP \n' + addrequest['error']['desc'] }
            return HttpResponse(json.dumps(msg))


class TrasladoUsuario(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            userid = Users.objects.get(pk=request.POST['user'])
            add = TrasladarForm(request.POST, instance=userid)
            if add.is_valid():
                name_municipio = list(Municipio.objects.filter(pk=request.POST['municipio']).values_list('municipio_name', flat=True))
                dataedit = {'municipio': name_municipio,}
                apipost = requests.put(settings.API_URL + "mail/modify/location/"+ request.POST['email'] + '/', data=dataedit)
                editrequest = apipost.json()
                if editrequest['status']:
                    add.save()

                    ip_address = request.META['REMOTE_ADDR']
                    msg_logs = 'El usuario %s %s (%s) traslado la cuenta (%s) desde %s' % (
                        request.user.first_name, request.user.last_name, request.user.email, request.POST['email'], request.POST['origen'])
                    Logs(users=request.user, ip=ip_address, comentario=msg_logs, msg_type=106).save()

                    msg = {'status': True, 'msg': 'Traslado de la cuenta completado'}
                    return HttpResponse(json.dumps(msg))
                else:
                    msg = {'status': False, 'msg': 'Ocurrio un error en LDAP\n' + editrequest['error']['desc']}
                    return HttpResponse(json.dumps(msg))
            else:
                msg = {'status': False, 'msg': 'Formulario no valido'}
                return HttpResponse(json.dumps(msg))
        else:
            msg = {'status': False, 'msg': 'Ocurrio un error'}
            return HttpResponse(json.dumps(msg))


class PassChange(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            user = Users.objects.get(pk=request.POST['user'])
            data = {'passwd': request.POST['passwd']}
            apipost = requests.put(settings.API_URL + "mail/modify/passwd/" + user.email + '/', data=data)
            addrequest = apipost.json()
            if addrequest['status']:
                ip_address = request.META['REMOTE_ADDR']
                msg_logs = 'El usuario %s %s (%s) cambio la clave de (%s)' % (request.user.first_name, request.user.last_name, request.user.email, user.email)
                Logs(users=request.user, ip=ip_address, comentario=msg_logs, msg_type=105).save()
                msg = {'status': True, 'msg': 'Contraseña modificada con exito'}
                return HttpResponse(json.dumps(msg))
            else:
                msg = {'status': False, 'msg': 'Ocurio un error en LDAP\n' + addrequest['error']['desc']}
                return HttpResponse(json.dumps(msg))


class EditUser(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            user = Users.objects.get(email=request.POST['email'])
            add = DatosPersonalesForm(request.POST, instance=user)
            if add.is_valid():
                name_ocupacion = list(Ocupacion.objects.filter(pk=request.POST['ocupacion']).values_list('ocupacion_name', flat=True))
                dataedit = {'nombre': request.POST['nombre'], 'apellidos': request.POST['apellidos'], 'ci': request.POST['ci'], 'ocupacion': name_ocupacion}
                apipost = requests.put(settings.API_URL + "mail/modify/data/"+ request.POST['email'] + '/', data=dataedit)
                editrequest = apipost.json()
                if editrequest['status']:
                    add.save()
                    ip_address = request.META['REMOTE_ADDR']
                    msg_logs = 'El usuario %s %s (%s) edito la cuenta (%s)' % (request.user.first_name, request.user.last_name, request.user.email, request.POST['email'])
                    Logs(users=request.user, ip=ip_address, comentario=msg_logs, msg_type=102).save()
                    
                    msg = {'status': True, 'msg': 'Usuario modificado con exito'}
                    return HttpResponse(json.dumps(msg))
                else:
                    msg = {'status': False, 'msg': 'Ocurrió un error en LDAP\n' + editrequest['error']['desc']}
                    return HttpResponse(json.dumps(msg))
            else:
                msg = {'status': False, 'msg': 'Formulario no valido'}
                return HttpResponse(json.dumps(msg))


@csrf_exempt
def update_estado_usuario(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        usuarioid = request.POST['id']
        estado = request.POST['estado']
        dataedit = {'estado': request.POST['estado_ldap']}
        apipost = requests.put(settings.API_URL + "mail/modify/status/"+ request.POST['email'] + '/', data=dataedit)
        editrequest = apipost.json()
        if editrequest['status']:
            updatenow = Users.objects.get(pk=usuarioid)
            updatenow.active = estado
            updatenow.save()
            return HttpResponse('1')
        else:
            return HttpResponse('2')
    else:
        return HttpResponse('2')


class ServiceChange(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            userid = Users.objects.get(pk=request.POST['user'])
            add = ServiceForm(request.POST, instance=userid)
            if add.is_valid():
                name_service = []
                for x in request.POST.getlist('sldservice'):
                    name_service += Services.objects.filter(pk=x).values_list('service', flat=True)
                dataedit = {'sldservice': name_service}
                apipost = requests.put(settings.API_URL + "mail/modify/service/"+ userid.email + '/', data=dataedit)
                editrequest = apipost.json()
                if editrequest['status']:
                    add.save()

                    ip_address = request.META['REMOTE_ADDR']
                    msg_logs = 'El usuario %s %s (%s) cambió los servicios de la cuenta (%s)' % (request.user.first_name, request.user.last_name, request.user.email, userid.email)
                    Logs(users=request.user, ip=ip_address, comentario=msg_logs, msg_type=102).save()

                    msg = {'status': True, 'msg': 'Servicios modificados con exitos'}
                    return HttpResponse(json.dumps(msg))
                else:
                    msg = {'status': False, 'msg': 'Ocurrio un error en LDAP\n' + editrequest['error']['desc']}
                    return HttpResponse(json.dumps(msg))
            else:
                msg = {'status': False, 'msg': 'Formulario no valido'}
                return HttpResponse(json.dumps(msg))
        else:
            msg = {'status': False, 'msg': 'Ocurrio un error'}
            return HttpResponse(json.dumps(msg))


class EditMail(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            user = Users.objects.get(email=request.POST['email'])
            add = DatosMailForm(request.POST, instance=user)
            if add.is_valid():                
                dataedit = {'tipo_cuenta': request.POST['tipo_cuenta'], 'quota': request.POST['quota']}
                apipost = requests.put(settings.API_URL + "mail/modify/email/"+ request.POST['email'] + '/', data=dataedit)
                editrequest = apipost.json()
                if editrequest['status']:
                    add.save()
                    ip_address = request.META['REMOTE_ADDR']
                    msg_logs = 'El usuario %s %s (%s) edito la cuenta (%s), cambió los datos del email' % (request.user.first_name, request.user.last_name, request.user.email, request.POST['email'])
                    Logs(users=request.user, ip=ip_address, comentario=msg_logs, msg_type=102).save()
                    
                    msg = {'status': True, 'msg': 'Datos de email modificado con exito'}
                    return HttpResponse(json.dumps(msg))
                else:
                    msg = {'status': False, 'msg': 'Ocurrió un error en LDAP\n' + editrequest['error']['desc']}
                    return HttpResponse(json.dumps(msg))
            else:
                msg = {'status': False, 'msg': 'Formulario no valido'}
                return HttpResponse(json.dumps(msg))


class AddDevice(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            device = DeviceForm(request.POST)
            user = Users.objects.get(pk=request.POST['user'])
            if device.is_valid():
                data = {'mac': request.POST['mac_address']}
                apipost = requests.put(settings.API_URL + "mail/modify/addmac/" + user.email + '/', data=data)
                addrequest = apipost.json()
                if addrequest['status']:
                    device.save()
                    ip_address = request.META['REMOTE_ADDR']
                    msg_logs = 'El usuario %s %s (%s) edito la cuenta (%s), agregó un dispositivo' % (
                    request.user.first_name, request.user.last_name, request.user.email, user.email)
                    Logs(users=request.user, ip=ip_address, comentario=msg_logs, msg_type=102).save()
                    
                    msg = {'status': True, 'msg': 'Dispositivo agregado correctamente'}
                    return HttpResponse(json.dumps(msg))
                else:
                    msg = {'status': False, 'msg': 'Ocurio un error en LDAP\n' + addrequest['error']['desc']}
                    return HttpResponse(json.dumps(msg))
            else:
                msg = {'status': False, 'msg': 'Formulario no valido'}
                return HttpResponse(json.dumps(msg))

@csrf_exempt
def wlan_check_mac(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            Device.objects.get(mac_address=request.POST['mac_address'])
            msg = {'valid': False}
        except:
            msg = {'valid': True}

        return HttpResponse(json.dumps(msg))


@csrf_exempt
def delete_mac_wlan(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {'mac': request.POST['mac']}
        apipost = requests.put(settings.API_URL + "mail/modify/delmac/" + request.POST['user'] + '/', data=data)
        addrequest = apipost.json()
        if addrequest['status']:
            ip_address = request.META['REMOTE_ADDR']            
            msg_logs = 'El usuario %s %s (%s) edito la cuenta (%s), eliminó un dispositivo' % (
                    request.user.first_name, request.user.last_name, request.user.email, request.POST['user'])
            Logs(users=request.user, ip=ip_address, comentario=msg_logs, msg_type=102).save()

            Device.objects.get(mac_address=request.POST['mac']).delete()
            
            msg = {'status': True, 'msg': 'Dispositivo borrado con exito'}
            return HttpResponse(json.dumps(msg))
        else:
            msg = {'status': False, 'msg': 'Ocurrió un error en LDAP\n' + addrequest['error']['desc']}
            return HttpResponse(json.dumps(msg))
    else:
        msg = {'status': False, 'msg': 'Formulario no valido'}
        return HttpResponse(json.dumps(msg))