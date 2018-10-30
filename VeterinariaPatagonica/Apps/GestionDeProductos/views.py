from django.template import loader
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from .models import Producto
from .forms import ProductoFormFactory
from VeterinariaPatagonica import tools

def producto(request):
    context = {}#Defino un contexto.
    template = loader.get_template('GestionDeProductos/GestionDeProductos.html')#Cargo el template desde la carpeta templates/GestionDeProductos.
    return HttpResponse(template.render(context, request))#Devuelvo la url con el template armado.

@login_required(redirect_field_name='proxima')
@permission_required('GestionDeProductos.add_Producto', raise_exception=True)
def modificar(request, id = None):
    producto = Producto.objects.get(id=id) if id is not None else None
    ProductoForm = ProductoFormFactory(producto)
    context = {'usuario' : request.user}

    if request.method == 'POST':
        formulario = ProductoForm(request.POST, instance=producto)
        if formulario.is_valid():
            producto = formulario.save()
            return HttpResponseRedirect("/GestionDeProductos/ver/{}".format(producto.id))
        else:
            context['formulario'] = formulario
    else:
        context['formulario'] = ProductoForm(instance=producto)
    template = loader.get_template('GestionDeProductos/formulario.html')

    return HttpResponse(template.render( context, request))

def verHabilitados(request):
    productos = Producto.objects.habilitados()
    productos = productos.filter(tools.paramsToFilter(request.GET, Producto))
    template = loader.get_template('GestionDeProductos/verHabilitados.html')
    context = {
        'productos': productos,
        'usuario': request.user
    }
    return HttpResponse(template.render(context, request))

def verDeshabilitados(request):
    productos = Producto.objects.deshabilitados()
    productos = productos.filter(tools.paramsToFilter(request.GET, Producto))
    template = loader.get_template('GestionDeProductos/verDeshabilitados.html')
    context = {
        'productos' : productos,
        'usuario' : request.user
    }
    return HttpResponse(template.render( context, request ))

def ver(request, id):
    #import ipdb; ipdb.set_trace()
    try:
        productos = Producto.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Http404( "No encontrado", "El Producto con id={} no existe.".format(id))

    template = loader.get_template('GestionDeProductos/ver.html')
    context = {
        'producto': productos,
        'usuario': request.user
    }
    return HttpResponse(template.render(context, request))


@login_required(redirect_field_name='proxima')
@permission_required('GestionDeProductos.delete_Producto', raise_exception=True)
def deshabilitar(request, id):

    try:
        producto = Producto.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Http404()

    producto.baja = True
    producto.save()

    return HttpResponseRedirect( "/GestionDeProductos/verDeshabilitados/" )


@login_required(redirect_field_name='proxima')
@permission_required('GestionDeProductos.delete_Producto', raise_exception=True)
def habilitar(request, id):
    try:
        producto = Producto.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Http404()

    producto.baja = False
    producto.save()

    return HttpResponseRedirect( "/GestionDeProductos/verHabilitados/" )


@login_required(redirect_field_name='proxima')
@permission_required('GestionDeProductos.delete_Producto', raise_exception=True)
def eliminar(request, id):

    try:
        producto = Producto.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Http404()

    if request.method == 'POST':
        producto.delete()
        return HttpResponseRedirect( "/GestionDeProductos/" )

    else:
        template = loader.get_template('GestionDeProductos/eliminar.html')
        context = {
            'usuario' : request.user,
            'id' : id
        }

        return HttpResponse( template.render( context, request) )





'''
def insumos(request):
    context = {}#Defino un contexto.
    template = loader.get_template('GestionDeProductos/GestionDeProductos.html')#Cargo el template desde la carpeta templates/GestionDeProductos.
    return HttpResponse(template.render(context, request))#Devuelvo la url con el template armado.
'''

'''
def alta(request):
    context = {}#Defino un contexto.
    template = loader.get_template('demos/altainsumo.html')#Cargo el template desde la carpeta demos.
    #template = loader.get_template('demos/altainsumo.html')#Cargo el template desde la carpeta demos.
    return HttpResponse(template.render(context,request))#Devuelvo la url con el template armado.
'''