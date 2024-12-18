from django.urls import path, include
from rest_framework.routers import DefaultRouter
from radius.api.views import UsersVS

router = DefaultRouter()

router.register('radius', UsersVS, basename='radius')

urlpatterns = [
    path('', include(router.urls)),
]