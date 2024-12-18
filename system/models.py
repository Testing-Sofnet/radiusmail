from django.db import models
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey

class Logs(models.Model):

    TYPE_MSG = (
        ('1', u'Login'),
        ('2', u'Logout'),
        ('3', u'Error'),
        ('4', u'Desactivada'),
        ('100', u'Cuenta Creada'),
        ('101', u'Cuenta Borrada'),
        ('102', u'Cuenta Modificada'),
        ('103', u'Cuenta Desactivada'),
        ('104', u'Cuenta Recuperada'),
        ('105', u'Cambio Password'),
        ('106', u'Traslado de cuenta'),
    )

    users = models.ForeignKey(User, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
    access_date = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField(blank=True)
    msg_type = models.CharField(max_length=3, choices=TYPE_MSG)

    def __str__(self):
        return "%s" % self.users

    class Meta:
        verbose_name_plural = 'Logs'


class Municipio(models.Model):
    municipio_name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.municipio_name

    class Meta:
        verbose_name_plural = 'Municipios'

class TipoTrabajo(models.Model):
    tipotrabajo = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.tipotrabajo

    class Meta:
        verbose_name_plural = 'Tipos de Trabajos'


class Trabajo(models.Model):
    municipio = models.ForeignKey(Municipio, related_name='TrabajoMunicipio', default=None, null=True, blank=True,
                                  on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoTrabajo, related_name='TrabajoTipoTrabajo', default=None, null=True, blank=True,
                             on_delete=models.CASCADE)
    trabajo_name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.trabajo_name

    class Meta:
        verbose_name_plural = 'Centro de Trabajo'


class UserProfile(models.Model):
    SEXO = (
        ('1', u'Masculino'),
        ('2', u'Femenino'),
    )
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    ci = models.CharField(max_length=11, help_text='Carne de Identidad')
    sexo = models.CharField(max_length=1, choices=SEXO, null=True, blank=True)
    municipio = models.ForeignKey(Municipio, related_name='UserProfileMunicipio', default=None, null=True, blank=True,
                                  on_delete=models.CASCADE)
    trabajo = ChainedForeignKey(Trabajo, chained_field="municipio", chained_model_field="municipio", default=None, null=True, blank=True)
    quota = models.IntegerField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(default=None, null=True, blank=True)

    def __str__(self):
        return u"%s" % self.user

    class Meta:
        verbose_name_plural = 'Datos de administracion'