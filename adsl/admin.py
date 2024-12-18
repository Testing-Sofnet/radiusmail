from django.contrib import admin
from .models import *

class EnlacesAdmin(admin.ModelAdmin):
    list_display = ('alias', 'trabajo', 'ipwan', 'ipwan_netmask', 'iplan', 'iplan_netmask', 'ed', 'tipo_conexion', 'municipio', 'enrutamiento')
    search_fields = ('alias', 'ipwan', 'iplan', 'ed')
    list_filter = ('tipo_conexion', 'enrutamiento')

class InternetAdmin(admin.ModelAdmin):
    list_display = ('adsl','fecha_autorizo', 'cuota', 'ip', 'municipio', 'trabajo', 'vencimiento', 'alerta_vencimiento')
    #search_fields = ('no',)
    #list_filter = ('suplemento',)

admin.site.register(Enlace, EnlacesAdmin)
admin.site.register(Internet, InternetAdmin)
