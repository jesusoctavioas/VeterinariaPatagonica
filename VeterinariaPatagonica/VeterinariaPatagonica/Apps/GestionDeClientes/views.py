from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def clientes(request):
    context = {}
    template = loader.get_template('GestionDeClientes/GestionDeClientes.html')
    return HttpResponse(template.render(context, request))
'''
def alta(request):
    context = {}
    template = loader.get_template('demos/altacliente.html')
'''
