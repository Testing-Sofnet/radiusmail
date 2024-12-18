import json
from django.utils.http import urlsafe_base64_decode
import datetime
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

from .models import *
#from contratos.models import Suplemento
from .forms import *
from system.decorators import group_required
from system.models import Logs, UserProfile, Municipio, TipoTrabajo


class AdslIndex(View):
    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user.pk)
        all_adsl = Enlace.objects.all()
        total = all_adsl.count()
        enrutado = all_adsl.filter(enrutamiento=True).count()
        internet = Internet.objects.all().count()
        #suplemento5 = Suplemento.objects.filter(suplemento=5).count()

        context_data = {
            'title': 'Enlaces dedicados',
            #'all_adsl': all_adsl,
            'user_profile': user_profile,
            'enlacesform': EnlacesForm(),
            'fecha': datetime.datetime.today(),
            'enrutado': enrutado,
            'total': total,
            'internet': internet,
            #'suplemento5': suplemento5,
        }
        return render(request, 'adsl/adsl_list.html', context_data)


@csrf_exempt
def adsl_check_ipwan(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            Enlace.objects.get(Q(ipwan=request.POST['ipwan']) | Q(iplan=request.POST['ipwan']))
            msg = {'valid': False}
        except:
            msg = {'valid': True}

        return HttpResponse(json.dumps(msg))


@csrf_exempt
def adsl_check_iplan(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            Enlace.objects.get(Q(ipwan=request.POST['iplan']) | Q(iplan=request.POST['iplan']))
            msg = {'valid': False}
        except:
            msg = {'valid': True}

        return HttpResponse(json.dumps(msg))


@csrf_exempt
def adsl_check_ipinternet(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            Internet.objects.get(Q(ip=request.POST['ip']))
            msg = {'valid': False}
        except:
            msg = {'valid': True}

        return HttpResponse(json.dumps(msg))


class AddEnlace(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            add = EnlacesForm(request.POST)
            if add.is_valid():
                datosp = add.save(commit=False)
                datosp.save()
                ip_address = request.META['REMOTE_ADDR']
                msg_logs = 'El usuario %s %s (%s) creo el enlace' % (
                    request.user.first_name, request.user.last_name, request.user.email)
                History(enlace=datosp, ip=ip_address, comentario=msg_logs, msg_type=200).save()
                messages.success(request, "Enlace creado correctamente")
                msg = {'status': True, 'msg': 'Enlace creado correctamente'}
                return HttpResponse(json.dumps(msg))
            else:
                msg = {'status': False, 'msg': 'Ocurrió un error'}
                return HttpResponse(json.dumps(msg))
        else:
            msg = {'status': False, 'msg': 'Ocurrió un error'}
            return HttpResponse(json.dumps(msg))


@csrf_exempt
def delete_enlace(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        enlaceid = request.POST['id']
        Enlace.objects.get(pk=enlaceid).delete()
        messages.success(request, "Enlace eliminado correctamente")
        msg = {'status': True, 'msg': 'Enlace eliminado correctamente'}
        return HttpResponse(json.dumps(msg))
    else:
        msg = {'status': False, 'msg': 'Ocurrió un error'}
        return HttpResponse(json.dumps(msg))


class EnlaceViewDate(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        munic = Municipio.objects.all().order_by('municipio_name')
        getenlace = get_object_or_404(Enlace, pk=urlsafe_base64_decode(kwargs['pk']))
        reportlog = History.objects.filter(enlace=getenlace).order_by('-pk')
        context = {'title': getenlace, 'getenlace': getenlace, 'reportlog': reportlog, 'munic': munic, 'asignarinternetform': AsignarInternetForm(), 'cambioipinternetform': CambioIpInternetForm(), 'cambioipform': CambioIPForm(instance=getenlace), 'cambioabform': CambioABForm(instance=getenlace), 'cambiotecform': CambioTecForm(instance=getenlace), 'trasladarform': TrasladarEnlaceForm(instance=getenlace), 'updateinternetform': UpdateInternetForm(instance=getenlace)}
        return render(request, 'adsl/adsl_edit.html', context)

@csrf_exempt
def route_enlace(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        enlaceid = request.POST['id']
        updatenow = Enlace.objects.get(pk=enlaceid)
        updatenow.enrutamiento = 1
        updatenow.save()
        ip_address = request.META['REMOTE_ADDR']
        msg_logs = 'El usuario %s %s (%s) enrutó el enlace (%s) ' % (
            request.user.first_name, request.user.last_name, request.user.email, updatenow.alias)
        History(enlace=updatenow, ip=ip_address, comentario=msg_logs, msg_type=207).save()
        messages.success(request, "Enlace enrutado correctamente")
        msg = {'status': True, 'msg': 'Enlace enrutado correctamente'}
        return HttpResponse(json.dumps(msg))
    else:
        msg = {'status': False, 'msg': 'Ocurrió un error'}
        return HttpResponse(json.dumps(msg))


class TrasladoEnlace(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            enlaceid = Enlace.objects.get(pk=request.POST['enlace'])
            add = TrasladarEnlaceForm(request.POST, instance=enlaceid)
            if add.is_valid():
                add.save()

                ip_address = request.META['REMOTE_ADDR']
                msg_logs = 'El usuario %s %s (%s) traslado el enlace (%s) desde %s ' % (
                    request.user.first_name, request.user.last_name, request.user.email, request.POST['alias-origen'], request.POST['origen'])
                History(enlace=enlaceid, ip=ip_address, comentario=msg_logs, msg_type=201).save()

                messages.success(request, "Traslado del enlace completado")

                msg = {'status': True, 'msg': 'Traslado del enlace completado'}
                return HttpResponse(json.dumps(msg))
            else:
                msg = {'status': False, 'msg': 'Ocurrio un error'}
                return HttpResponse(json.dumps(msg))
        else:
            msg = {'status': False, 'msg': 'Ocurrio un error'}
            return HttpResponse(json.dumps(msg))

class CambioBloqueIP(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            enlaceid = Enlace.objects.get(pk=request.POST['enlace'])
            add = CambioIPForm(request.POST, instance=enlaceid)
            if add.is_valid():
                add.save()

                ip_address = request.META['REMOTE_ADDR']
                msg_logs = 'El usuario %s %s (%s) cambió el bloque IP LAN (%s) ' % (
                    request.user.first_name, request.user.last_name, request.user.email, request.POST['origen-ip'])
                History(enlace=enlaceid, ip=ip_address, comentario=msg_logs, msg_type=202).save()

                messages.success(request, "Cambio de bloque IP LAN completado")

                msg = {'status': True, 'msg': 'Cambio de bloque IP LAN completado'}
                return HttpResponse(json.dumps(msg))
            else:
                msg = {'status': False, 'msg': 'Ocurrio un error'}
                return HttpResponse(json.dumps(msg))
        else:
            msg = {'status': False, 'msg': 'Ocurrio un error'}
            return HttpResponse(json.dumps(msg))

class CambioAB(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            enlaceid = Enlace.objects.get(pk=request.POST['enlace'])
            add = CambioABForm(request.POST, instance=enlaceid)
            if add.is_valid():
                add.save()

                ip_address = request.META['REMOTE_ADDR']
                msg_logs = 'El usuario %s %s (%s) cambió el Ancho de Banda (%s) ' % (
                    request.user.first_name, request.user.last_name, request.user.email, request.POST['origen-ab'])
                History(enlace=enlaceid, ip=ip_address, comentario=msg_logs, msg_type=203).save()

                messages.success(request, "Cambio de Ancho de Banda completado")

                msg = {'status': True, 'msg': 'Cambio de Ancho de Banda completado'}
                return HttpResponse(json.dumps(msg))
            else:
                msg = {'status': False, 'msg': 'Ocurrio un error'}
                return HttpResponse(json.dumps(msg))
        else:
            msg = {'status': False, 'msg': 'Ocurrio un error'}
            return HttpResponse(json.dumps(msg))

class CambioTec(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            enlaceid = Enlace.objects.get(pk=request.POST['enlace'])
            add = CambioTecForm(request.POST, instance=enlaceid)
            if add.is_valid():
                add.save()

                ip_address = request.META['REMOTE_ADDR']
                msg_logs = 'El usuario %s %s (%s) cambió la tecnologia (%s) ' % (
                    request.user.first_name, request.user.last_name, request.user.email, request.POST['origen-tec'])
                History(enlace=enlaceid, ip=ip_address, comentario=msg_logs, msg_type=205).save()

                messages.success(request, "Cambio de tecnología completado")

                msg = {'status': True, 'msg': 'Cambio de tecnología completado'}
                return HttpResponse(json.dumps(msg))
            else:
                msg = {'status': False, 'msg': 'Ocurrio un error'}
                return HttpResponse(json.dumps(msg))
        else:
            msg = {'status': False, 'msg': 'Ocurrio un error'}
            return HttpResponse(json.dumps(msg))

class CambioIPInternet(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            internetid = Internet.objects.get(pk=request.POST['internet'])
            enlaceid = Enlace.objects.get(pk=request.POST['enlace'])
            add = CambioIpInternetForm(request.POST, instance=internetid)
            if add.is_valid():
                add.save()

                ip_address = request.META['REMOTE_ADDR']
                msg_logs = 'El usuario %s %s (%s) cambió la IP de internet (%s) ' % (
                    request.user.first_name, request.user.last_name, request.user.email, request.POST['origen-ip-internet'])
                History(enlace=enlaceid, ip=ip_address, comentario=msg_logs, msg_type=206).save()

                messages.success(request, "Cambio de IP con Internet completado")

                msg = {'status': True, 'msg': 'Cambio de IP con Internet completado'}
                return HttpResponse(json.dumps(msg))
            else:
                msg = {'status': False, 'msg': 'Ocurrio un error'}
                return HttpResponse(json.dumps(msg))
        else:
            msg = {'status': False, 'msg': 'Ocurrio un error'}
            return HttpResponse(json.dumps(msg))

class AsignarInternet(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            enlaceid = Enlace.objects.get(pk=request.POST['enlace'])
            add = AsignarInternetForm(request.POST)
            if add.is_valid():
                datosint = add.save(commit=False)
                datosint.municipio = enlaceid.municipio
                datosint.trabajo = enlaceid.trabajo
                datosint.adsl = enlaceid
                datosint.save()

                ip_address = request.META['REMOTE_ADDR']
                msg_logs = 'El usuario %s %s (%s) Asignó internet al enlace por la ip (%s) ' % (
                    request.user.first_name, request.user.last_name, request.user.email, request.POST['ip'])
                History(enlace=enlaceid, ip=ip_address, comentario=msg_logs, msg_type=204).save()

                messages.success(request, "Asignado servicio de internet")

                msg = {'status': True, 'msg': 'Asignado servicio de internet'}
                return HttpResponse(json.dumps(msg))
            else:
                msg = {'status': False, 'msg': 'Ocurrio un error'}
                return HttpResponse(json.dumps(msg))
        else:
            msg = {'status': False, 'msg': 'Ocurrio un error'}
            return HttpResponse(json.dumps(msg))

class InternetIndex(View):
    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user.pk)

        context_data = {
            'title': 'Permisos de Internet',
            'user_profile': user_profile,
            #'updateinternetform': UpdateInternetForm,
            #'fecha': datetime.datetime.today(),
        }
        return render(request, 'adsl/internet_list.html', context_data)


class ActualizarPermiso(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            internetid = Internet.objects.get(pk=request.POST['internet'])
            enlaceid = Enlace.objects.get(pk=request.POST['enlace'])
            add = UpdateInternetForm(request.POST, instance=internetid)
            if add.is_valid():
                add.save()

                ip_address = request.META['REMOTE_ADDR']
                msg_logs = 'El usuario %s %s (%s) actualizó el permiso de internet ' % (
                    request.user.first_name, request.user.last_name, request.user.email)
                History(enlace=enlaceid, ip=ip_address, comentario=msg_logs, msg_type=208).save()

                messages.success(request, "Permiso de Internet Actualizado")

                msg = {'status': True, 'msg': 'Permiso de Internet Actualizado'}
                return HttpResponse(json.dumps(msg))
            else:
                msg = {'status': False, 'msg': 'Ocurrio un error'}
                return HttpResponse(json.dumps(msg))
        else:
            msg = {'status': False, 'msg': 'Ocurrio un error'}
            return HttpResponse(json.dumps(msg))