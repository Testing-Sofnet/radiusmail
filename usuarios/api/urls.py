from django.urls import path, include
from rest_framework.routers import DefaultRouter
from usuarios.api.views import UsuarioVS

router = DefaultRouter()

router.register('usuarios', UsuarioVS, basename='usuarios')

urlpatterns = [
    path('', include(router.urls)),
]
