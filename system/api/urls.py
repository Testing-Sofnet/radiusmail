from django.urls import path, include
from rest_framework.routers import DefaultRouter
from system.api.views import LogsVS

router = DefaultRouter()

router.register('logs', LogsVS, basename='logs')

urlpatterns = [
    path('', include(router.urls)),
]