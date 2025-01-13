from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from certificados.api import viewsets as certificadosviewsets

route = routers.DefaultRouter()

route.register(r'certificados', certificadosviewsets.CertificadoViewSet,
               basename='Certificados')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(route.urls)),
]
