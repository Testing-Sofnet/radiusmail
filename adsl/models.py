from django.db import models
from system.models import Trabajo, Municipio
import datetime


class Enlace(models.Model):
    TYPE_CONEXION = (
        ('adsl', u'ADSL'),
        ('fibra', u'Fibra Optica'),
    )
    TYPE_AB = (
        ('Kbps', u'Kbps'),
        ('Mbps', u'Mbps'),
        ('Gbps', u'Gbps'),
    )
    NET_MASK_WAN = (
        ('/30', u'/30'),
        ('/32', u'/32'),
    )
    NET_MASK_LAN = (
        ('/24', u'/24'),
        ('/25', u'/25'),
        ('/26', u'/26'),
        ('/27', u'/27'),
        ('/28', u'/28'),
        ('/29', u'/29'),
        ('/30', u'/30'),
    )
    alias = models.CharField(max_length=255, verbose_name='Alias del enlace')
    ipwan = models.GenericIPAddressField(default=None, null=True, blank=True, verbose_name='Bloque IP WAN')
    ipwan_netmask = models.CharField(max_length=3, choices=NET_MASK_WAN, verbose_name='Mascara')
    iplan = models.GenericIPAddressField(default=None, null=True, blank=True, verbose_name='Bloque IP LAN')
    iplan_netmask = models.CharField(max_length=3, choices=NET_MASK_LAN, verbose_name='Mascara', null=True,
                                     blank=True, )
    ed = models.CharField(max_length=100, verbose_name='ED')
    ab = models.CharField(max_length=50, verbose_name='Ancho de Banda')
    um_ab = models.CharField(max_length=4, choices=TYPE_AB)
    tipo_conexion = models.CharField(max_length=5, choices=TYPE_CONEXION, verbose_name='Tipo de conexión')
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, default=None, null=True, blank=True)
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE, default=None, null=True, blank=True)
    enrutamiento = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True, null=False)
    modify_date = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.alias

    class Meta:
        verbose_name_plural = 'Enlaces dedicados'


class Internet(models.Model):
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=False)
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE, null=False)
    adsl = models.OneToOneField(Enlace, null=False, on_delete=models.CASCADE, related_name='InternetAdsl')
    fecha_autorizo = models.DateField(default=None, null=True)
    cuota = models.CharField(max_length=6, null=True, verbose_name='Cuota de Internet (MB)')
    create_date = models.DateTimeField(auto_now_add=True, null=False)
    modify_date = models.DateTimeField(auto_now=True, null=False)
    ip = models.GenericIPAddressField(default=None, null=True, blank=True, verbose_name='IP con Internet')

    def vencimiento(self):
        fecha_vencido = self.fecha_autorizo + datetime.timedelta(days=730)
        return fecha_vencido

    def alerta_vencimiento(self):
        time1 = self.fecha_autorizo + datetime.timedelta(days=700)
        time2 = self.fecha_autorizo + datetime.timedelta(days=730)
        if time1 <= datetime.datetime.now().date() < time2:
            return "warning"
        elif time2 <= datetime.datetime.now().date():
            return "danger"

    def __str__(self):
        return self.adsl.alias

    class Meta:
        verbose_name_plural = 'Servicio Internet'


class History(models.Model):
    TYPE_MSG = (
        ('200', u'Creado'),
        ('201', u'Traslado'),
        ('202', u'Cambio de IP'),
        ('203', u'Cambio de AB'),
        ('204', u'Internet Asignado'),
        ('205', u'Cambio de tecnologia'),
        ('206', u'Cambio de IP de Internet'),
        ('207', u'Enrutado'),
        ('208', u'Permiso de Internet Actualizado'),
    )
    enlace = models.ForeignKey(Enlace, on_delete=models.CASCADE, related_name='EnlaceHistory', default=None, null=True,
                               blank=True)
    ip = models.GenericIPAddressField()
    access_date = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField(blank=True)
    msg_type = models.CharField(max_length=3, choices=TYPE_MSG)

    def __str__(self):
        return self.enlace

    class Meta:
        verbose_name_plural = 'History'
