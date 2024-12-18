from django.db import models
from system.models import Municipio, Trabajo


class Ocupacion(models.Model):
    ocupacion_name = models.CharField(max_length=150, blank=False)

    def __str__(self):
        return self.ocupacion_name

    class Meta:
        verbose_name_plural = 'Ocupacion'


class Services(models.Model):
    service_name = models.CharField(max_length=20, blank=False)
    service = models.CharField(max_length=20, blank=False)
    service_active = models.BooleanField(default=True)

    def __str__(self):
        return self.service_name

    class Meta:
        verbose_name_plural = 'Servicios'


class Users(models.Model):

    TYPE_CHOICES = (
        ('Personal', u'Personal'),
        ('Institucional', u'Institucional'),
    )

    email = models.CharField(max_length=50, db_index=True)
    nombre = models.CharField(max_length=50, blank=False)
    apellidos = models.CharField(max_length=100, blank=False)
    ci = models.CharField(max_length=11, help_text='Carne de Identidad', db_index=True)
    sexo = models.CharField(max_length=50, default=None, null=True, blank=True)
    address = models.CharField(max_length=255, blank=False)
    quota = models.IntegerField(blank=False, help_text='Numero en Mb')
    telefono = models.CharField(max_length=11, default=None, null=True, blank=True)
    telefono_work = models.CharField(max_length=11, default=None, null=True, blank=True)
    tipo_cuenta = models.CharField(max_length=13, choices=TYPE_CHOICES)
    notas = models.TextField(blank=True)
    municipio = models.ForeignKey(Municipio, related_name='UsersMunicipio', null=True, on_delete=models.SET_NULL)
    trabajo = models.ForeignKey(Trabajo, related_name='UsersTrabajo', null=True, on_delete=models.SET_NULL)
    ocupacion = models.ForeignKey(Ocupacion, related_name='UsersOcupacion', null=True, on_delete=models.SET_NULL)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    expire_date = models.DateField(default=None, null=True, blank=True)
    active = models.BooleanField(default=True)
    mark_delete = models.BooleanField(default=False)
    sldservice = models.ManyToManyField(Services, related_name='UsersService')
    uidNumber = models.IntegerField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        s = self.ci[9]
        if int(s) % 2 == 0:
            self.sexo = "Masculino"
            super(Users, self).save(*args, **kwargs)
        else:
            self.sexo = "Femenino"
            super(Users, self).save(*args, **kwargs)
        

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'Usuarios'


class Device(models.Model):

    TYPE_DEVICE = (
        ('1', u'Laptop'),
        ('2', u'Tablet'),
        ('3', u'Movil'),
    )

    TYPE_OS = (
        ('1', u'Windows'),
        ('2', u'iOS'),
        ('3', u'Android'),
        ('4', u'Linux'),
        ('5', u'Mac OXS'),
    )

    model = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    type_device = models.CharField(max_length=1, choices=TYPE_DEVICE)
    mac_address = models.CharField(max_length=100)
    os = models.CharField(max_length=1, choices=TYPE_OS)
    user = models.ForeignKey(Users, related_name='DeviceUsers', on_delete=models.CASCADE)

    def __str__(self):
        return u"%s - %s" % (self.user.nombre, self.type_device)

    class Meta:
        verbose_name_plural = 'Dispositivos'

