"""radiusmail URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from system.views import Login, Logout, Dashboard, Profile


urlpatterns = [
    path('admin/', admin.site.urls),
    path('chaining/', include('smart_selects.urls')),
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('dashboard/', login_required(Dashboard.as_view(), login_url='login'), name='dashboard'),
    path('profile/', login_required(Profile.as_view(), login_url='login'), name='profile'),
    path('system/', include('system.urls')),
    path('users/', include('usuarios.urls')),
    path('radius/', include('radius.urls')),
    path('adsl/', include('adsl.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('api_users/', include('usuarios.api.urls')),
    path('api_logs/', include('system.api.urls')),
    path('api_radius/', include('radius.api.urls')),
    path('api_adsl/', include('adsl.api.urls')),
]
