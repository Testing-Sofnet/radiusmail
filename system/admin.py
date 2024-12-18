from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User
from .models import Logs, UserProfile, Municipio, Trabajo, TipoTrabajo

class UserProfileInline(admin.TabularInline):
    model = UserProfile
    max_num = 1

class UserAdmin(DjangoUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'first_name', 'last_name', 'email', 'last_login', 'is_staff', 'is_active')

class LogsAdmin(admin.ModelAdmin):
    list_display = ('users', 'ip', 'access_date', 'msg_type', 'comentario')
    search_fields = ('comentario',)
    list_filter = ('msg_type',)

class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('municipio_name',)

class TipoTrabajoAdmin(admin.ModelAdmin):
    list_display = ('tipotrabajo',)

class TrabajoAdmin(admin.ModelAdmin):
    list_display = ('trabajo_name', 'tipo', 'municipio')
    search_fields = ('trabajo_name',)
    list_filter = ('municipio', 'tipo')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Logs, LogsAdmin)
admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(TipoTrabajo, TipoTrabajoAdmin)
admin.site.register(Trabajo, TrabajoAdmin)
