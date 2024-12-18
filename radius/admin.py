from django.contrib import admin
from .models import Users, Group

class UsersAdmin(admin.ModelAdmin):
    list_display = ('name','email','create_date', 'expire_date', 'group')

class GroupsAdmin(admin.ModelAdmin):
    list_display = ('group_name','group_active')

admin.site.register(Users, UsersAdmin)
admin.site.register(Group, GroupsAdmin)
