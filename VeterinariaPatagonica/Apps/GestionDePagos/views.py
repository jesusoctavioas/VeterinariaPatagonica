from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, permission_required
from .models import Pago
#from .forms import PagoFormFactory
from .forms import PagoForm
from Apps.GestionDeFacturas.models import Factura
from VeterinariaPatagonica import tools



def pago(request):

    context = {}#Defino el contexto.
    template = loader.get_template('GestionDePagos/GestionDePagos.html')#Cargo el template desde la carpeta templates/GestionDePagos.
    return HttpResponse(template.render(context, request))#Devuelvo la url con el template armado.


@login_required(redirect_field_name='proxima')
@permission_required('GestionDePagos.add_Pago', raise_exception=True)
def modificar(request, id = None): #, factura_id=None

    pago = Pago.objects.get(id=id) if id is not None else None
    context = {'usuario': request.user}

    if request.method == 'POST':
        formulario = PagoForm(request.POST, instance=pago)
        #print(formulario)
        if formulario.is_valid():
            pago = formulario.save()
            return HttpResponseRedirect("/GestionDePagos/ver/{}".format(pago.id))
        else:
            context['formulario'] = formulario
    else:
        context['formulario'] = PagoForm(instance=pago)
    template = loader.get_template('GestionDePagos/formulario.html')
    return HttpResponse(template.render(context, request))

    '''factura = None
    if factura_id:
        factura = Factura.objects.get(pk=factura_id)
    PagoForm = PagoFormFactory(pago, factura)'''





@login_required(redirect_field_name='proxima')
@permission_required('GestionDePagos.delete_Pago', raise_exception=True)
def eliminar(request, id):

    try:
        pago = Pago.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Http404()

    if request.method == 'POST':

        pago.delete()
        return HttpResponseRedirect( "/GestionDePagos/" )

    else:

        template = loader.get_template('GestionDePagos/eliminar.html')
        context = {
            'usuario' : request.user,
            'id' : id
        }

        return HttpResponse( template.render( context, request) )

def ver(request, id):

    try:
        pago = Pago.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Http404("No encontrado", "El pago con id={} no existe.".format(id))

    template = loader.get_template('GestionDePagos/ver.html')
    contexto = {
        'pago': pago,
        'usuario': request.user
    }

    return HttpResponse(template.render(contexto, request))

def listar(request):
    pagos = Pago.objects.all()
    pagos = pagos.filter(tools.paramsToFilter(request.GET, Pago))
    template = loader.get_template('GestionDePagos/listar.html')
    contexto = {
        'pagos' : pagos,
        'usuario' : request.user,
    }
    return  HttpResponse(template.render(contexto, request))
