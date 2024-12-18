import json
from django.utils.http import urlsafe_base64_decode

import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from django.conf import settings
from django.views.generic import View, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Users, Group
from .forms import UsersRadiusForm
from system.decorators import group_required
from system.models import Logs


class RadiusIndex(View):
    def get(self, request):


        context_data = {
            'title': 'Radius',
            'userform': UsersRadiusForm(),
        }
        return render(request, 'radius/radius.html', context_data)

@csrf_exempt
def radius_check_mail(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            Users.objects.get(email=request.POST['email'])
            msg = {'valid': False}
        except:
            msg = {'valid': True}

        return HttpResponse(json.dumps(msg))

class AddRadius(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            user = request.user
            add = UsersRadiusForm(request.POST)
            if add.is_valid():                
                group = Group.objects.get(pk=request.POST['group'])
                dataadd = {'name': request.POST['name'], 'email': request.POST['email'], 'group': group.group_name,
                           'description': request.POST['description'], 'passwd': request.POST['passwd1']}
                apipost = requests.post(settings.API_URL + "radius/add/", data=dataadd)
                addrequest = apipost.json()
                if addrequest['status']:
                    add.save()
                    ip_address = request.META['REMOTE_ADDR']
                    msg_logs = 'El usuario %s %s (%s) creo la cuenta %s de Radius' % (
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

class RadiusViewDate(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        getuser = get_object_or_404(Users, pk=urlsafe_base64_decode(kwargs['pk']))
        context = {'title': getuser, 'getuser': getuser, 'userform': UsersRadiusForm(instance=getuser),}
        return render(request, 'radius/radius_edit.html', context)


@csrf_exempt
def delete_users_radius(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        apipost = requests.delete(settings.API_URL + "radius/delete/" + request.POST['user'] + '/')
        addrequest = apipost.json()
        if addrequest['status']:
            ip_address = request.META['REMOTE_ADDR']
            msg_logs = 'El usuario %s %s (%s) borro la cuenta %s de Radius' % (
            request.user.first_name, request.user.last_name, request.user.email, request.POST['user'])
            Logs(users=request.user, ip=ip_address, comentario=msg_logs, msg_type=101).save()

            Users.objects.get(email=request.POST['user']).delete()
            messages.success(request, "Usuario eliminado correctamente")
            msg = {'status': True, 'msg': 'Usuario eliminado con exito'}
            return HttpResponse(json.dumps(msg))
        else:
            msg = {'status': False, 'msg': 'Ocurrió un error en LDAP \n' + addrequest['error']['desc'] }
            return HttpResponse(json.dumps(msg))


class PassRadius(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            user = Users.objects.get(pk=request.POST['user'])
            data = {'passwd': request.POST['passwd']}
            apipost = requests.put(settings.API_URL + "radius/modify/passwd/" + user.email + '/', data=data)
            addrequest = apipost.json()
            if addrequest['status']:
                ip_address = request.META['REMOTE_ADDR']
                msg_logs = 'El usuario %s %s (%s) cambio la clave de %s de Radius' % (
                request.user.first_name, request.user.last_name, request.user.email, user.email)
                Logs(users=request.user, ip=ip_address, comentario=msg_logs, msg_type=105).save()                
                msg = {'status': True, 'msg': 'Contraseña modificada con exito'}
                return HttpResponse(json.dumps(msg))
            else:
                msg = {'status': False, 'msg': 'Ocurio un error en LDAP\n' + addrequest['error']['desc']}
                return HttpResponse(json.dumps(msg))


class EditRadius(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            user = Users.objects.get(email=request.POST['email'])
            add = UsersRadiusForm(request.POST, instance=user)
            if add.is_valid():
                group = Group.objects.get(pk=request.POST['group'])
                dataedit = {'name': request.POST['name'], 'group': group.group_name , 'description': request.POST['description']}
                apipost = requests.put(settings.API_URL + "radius/modify/data/"+ request.POST['email'] + '/', data=dataedit)
                editrequest = apipost.json()
                if editrequest['status']:
                    add.save()
                    ip_address = request.META['REMOTE_ADDR']
                    msg_logs = 'El usuario %s %s (%s) edito la cuenta %s de Radius' % (
                    request.user.first_name, request.user.last_name, request.user.email, request.POST['email'])
                    Logs(users=request.user, ip=ip_address, comentario=msg_logs, msg_type=102).save()
                    
                    msg = {'status': True, 'msg': 'Usuario modificado con exito'}
                    return HttpResponse(json.dumps(msg))
                else:
                    msg = {'status': False, 'msg': 'Ocurrió un error en LDAP\n' + editrequest['error']['desc']}
                    return HttpResponse(json.dumps(msg))
            else:
                msg = {'status': False, 'msg': 'Formulario no valido'}
                return HttpResponse(json.dumps(msg))