from django.urls import path, include
from rest_framework.routers import DefaultRouter
from adsl.api.views import EnlaceVS, InternetVS

router = DefaultRouter()

router.register('adsl', EnlaceVS, basename='adsl')
router.register('internet', InternetVS, basename='internet')

urlpatterns = [
    path('', include(router.urls)),
]