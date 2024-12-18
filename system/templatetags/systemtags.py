from django import template
from django.http import request
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.models import Group
from django.utils.encoding import force_bytes, force_str
import datetime


#tags
def do_users(parser, token):
    return DefaultUsers()


class DefaultUsers(template.Node):
    def render(self, context):
        Users = None
        try:
            Users = context['user']
        except Users.DoesNotExist:
            pass

        context['user_datos'] = Users

        return ''

#filters
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

def quota(val_quota, val):
    return int(val)*100/int(val_quota)

def quota_style(val_quota):
    if val_quota <= 50:
        return 'bg-success'
    if val_quota >= 51 and val_quota <= 80:
        return 'bg-warning'
    if val_quota > 80:
        return 'bg-danger'

def encode_url(url):
    return urlsafe_base64_encode(force_bytes(url))


register = template.Library()

def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)

register.simple_tag(current_time)

register.tag('get_users_datos', do_users)

register.filter('has_group', has_group)
register.filter('quota', quota)
register.filter('quota_style', quota_style)
register.filter('encode_url', encode_url)