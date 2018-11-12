from django.db import models
#from Apps.GestionDePagos import models as pagModel
from Apps.GestionDeProductos import models as proModel
from Apps.GestionDeClientes import models as cliModel
from django.core.validators import RegexValidator
from decimal import Decimal
from django.db.models import Q
from django.utils import timezone as djangotimezone
# Create your models here.

# Create your models here.

REGEXTIPO = '^[A-B-C]{1}$'
MAXTIPO = 1
MAXDECIMAL = 2
MAXDIGITO = 6

MAX_DIGITOS_AJUSTES = 5
MAX_DECIMALES_AJUSTES = 2

class Factura(models.Model):

    MAPPER = {
        "tipo": "tipo__icontains",
        "cliente": lambda value: Q(cliente__nombres__icontains=value) | Q(cliente__apellidos__icontains=value),
        "fecha": "fecha_icontains"
    }

    tipo = models.CharField(
        help_text= "Tipo de Factura.",
        max_length=MAXTIPO,
        unique=False,
        null=False,
        blank=False,
        validators=[RegexValidator(regex=REGEXTIPO)],
        error_messages={
            'max_length': "El tipo de factura puede tener a lo sumo {} caracteres".format(MAXTIPO),
            'blank': "El tipo es obligatorio"
        }
    )

    cliente = models.ForeignKey(
        cliModel.Cliente,
        unique=False,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        error_messages={
            'blank': "El cliente es obligatorio"
        }
    )

    fecha = models.DateField(
        help_text="Fecha de la Factura.",
        unique=False,
        null=False,
        blank=False,
        default=djangotimezone.now,
        error_messages={
            'blank': "La fecha es obligatoria"
        }
    )

    detalles = models.ManyToManyField(
        proModel.Producto,
        through='DetalleFactura',

    )

    total = models.IntegerField(
        help_text="Importe total de la Factura.",
        unique=False,
        null=False,
        default=0.0,
        blank=False,
        error_messages={
            'blank': "El importe es obligatorio"
        }
    )
    recargo = models.DecimalField(
            blank=False,
            null = False,
            default=Decimal(0),
            max_digits = MAX_DIGITOS_AJUSTES,
            decimal_places = MAX_DECIMALES_AJUSTES,
            error_messages = {},
            validators = []
    )

    descuento = models.DecimalField(
            blank=False,
            null = False,
            default=Decimal(0),
            max_digits = MAX_DIGITOS_AJUSTES,
            decimal_places = MAX_DECIMALES_AJUSTES,
            error_messages = {},
            validators = []
    )

    productos = models.ForeignKey(
        praModel.Practica,
        unique=False,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        error_messages={
            'blank': "El producto es obligatorio"
        }


    )



    #pago = models.OneToOneField(
    #hel_text="Pago de la Factura.",
    #through='pagModel.Pago',
    #)

    baja = models.BooleanField(default=False)

    def __str__(self):
        cadena = 'Tipo de Factura: {0}, Cliente: {1} Total: {2}.'
        return cadena.format(self.tipo, self.cliente, self.total)

    def precioTotal(self):
        total = Decimal("0")
        for detalle in self.detalles.all():
            total += detalle.subtotal
        return total

    def calcular_subtotales(self, detalles):
        self.total = Decimal("0")
        self.save()
        for detalle in detalles:
            detalle.factura = self
            detalle.save()
            self.total += detalle.subtotal
        self.save()


    '''def  __unicode__(self):
        return self.total'''

class DetalleFactura(models.Model):
    factura = models.ForeignKey(
        Factura,
        on_delete=models.CASCADE,
        help_text="Ingrese numero de Factura",
        unique=False,
        null=False,
        blank=False,
        error_messages={
            'blank': "La Factura es obligatoria"
        }
    )

    producto = models.ForeignKey(
        proModel.Producto,
        on_delete=models.CASCADE,
        #help_text="Ingrese Producto",
        unique=False,
        null=False,
        blank=False,
        error_messages={
            'blank': "Debe ingresar al menos un producto"
        }
    )
    cantidad = models.IntegerField(
        #help_text="Ingrese Cantidad",
        unique=False,
        null=False,
        blank=False,
        error_messages={
            'blank': "La cantidad es obligatoria"
        }
    )
    subtotal = models.DecimalField(
        null= True,
        #help_text="Ingrese precio del producto",
        max_digits= MAXDIGITO,
        decimal_places= MAXDECIMAL,
    )

    def  __unicode__(self):
        return self.subtotal



    def save(self, *args, **kwargs):
        if (not "commit" in kwargs) or (kwargs["commit"]):
            if (self.subtotal is None):
                precio = self.producto.precioPorUnidad
                self.subtotal = precio * self.cantidad
                print("Precio: {}, Cantidad: {}, Subtotal: {}".format(precio, self.cantidad, self.subtotal))

        super().save(*args, **kwargs)
