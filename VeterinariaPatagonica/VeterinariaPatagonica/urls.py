"""VeterinariaPatagonica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls import url
from . import views
urlpatterns = [
    #path(r'admin/', admin.site.urls),
    #url(r'^$',, name='base')
    #url(r'test/', include("Apps.GestionDeClientes.urls"))

    url(r'^$',views.base),#Definimos la url del sitio base.
    path(r'GestionDeServicios/', include('VeterinariaPatagonica.Apps.GestionDeServicios.urls', namespace= 'servicios')),#Definimos que la url "GestionDeServicios" incluye todas las url que hay en GestionDeServicios.urls
    path(r'GestionDeClientes/', include('VeterinariaPatagonica.Apps.GestionDeClientes.urls', namespace= 'clientes')),#Definimos que la url "GestionDeClientes" incluye todas las url que hay en GestionDeClientes.urls
    #url(r'GestionDeInsumos/$',insumos_views.insumos , name='insumos'),
    path(r'GestionDeInsumos/',include('VeterinariaPatagonica.Apps.GestionDeInsumos.urls', namespace='insumos')),#Definimos que la url "GestionDeInsumos" incluye todas las url que hay en GestionDeInsumos.urls
    path(r'GestionDeMascotas/', include('VeterinariaPatagonica.Apps.GestionDeMascotas.urls', namespace= 'mascotas')),#Definimos que la url "GestionDeMascotas" incluye todas las url que hay en GestionDeMascotas.url
]
