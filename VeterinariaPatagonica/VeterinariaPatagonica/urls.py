from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from . import views

app_name ='bases'

urlpatterns = [


    #path('accounts/', include('django.contrib.auth.urls')),

    url(r'^$', views.index, name='index'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('admin/', admin.site.urls),
    #url(r'^$',, name='base')
    #url(r'test/', include("Apps.GestionDeClientes.urls"))
    #url(r'.*/login.html', views.login),
    #url(r'^$',views.base),#Definimos la url del sitio base.
    path(r'GestionDeServicios/', include('Apps.GestionDeServicios.urls', namespace= 'servicios')),#Definimos que la url "GestionDeServicios" incluye todas las url que hay en GestionDeServicios.urls
    path(r'GestionDeClientes/', include('Apps.GestionDeClientes.urls', namespace= 'clientes')),#Definimos que la url "GestionDeClientes" incluye todas las url que hay en GestionDeClientes.urls
    path(r'GestionDeInsumos/',include('Apps.GestionDeInsumos.urls', namespace='insumos')),#Definimos que la url "GestionDeInsumos" incluye todas las url que hay en GestionDeInsumos.urls
    path(r'GestionDeMascotas/', include('Apps.GestionDeMascotas.urls', namespace= 'mascotas')),#Definimos que la url "GestionDeMascotas" incluye todas las url que hay en GestionDeMascotas.url
    path(r'GestionDePracticas/', include('Apps.GestionDePracticas.urls', namespace='practicas')),
    #path(r'GestionTiposDeAtencion',include('Apps.GestionDeTiposDeAtencion', namespace= 'tiposdeatencion')),
    path(r'GestionDeTiposDeAtencion/',include('Apps.GestionDeTiposDeAtencion.urls', namespace= 'tiposdeatencion')),
]
