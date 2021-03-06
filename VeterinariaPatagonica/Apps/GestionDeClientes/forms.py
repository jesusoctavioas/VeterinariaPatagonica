from django import forms
from .models import Cliente
from localflavor.ar import forms as lforms
from django.core.validators import RegexValidator
#Para que no pinche instalar -> pip install django-localflavor


def ClienteFormFactory(cliente=None):
    campos = [  'tipoDeCliente',
                'nombres', 'apellidos',
                'direccion', 'localidad',
                'celular', 'telefono',
                'email',
                'descuentoServicio', 'descuentoProducto', 'cuentaCorriente']

    if cliente is None:
        campos.insert(1, 'dniCuit')

    class ClienteForm(forms.ModelForm):

        class Meta:
            model = Cliente
            fields = campos
            labels = {
                'dniCuit':'Dni/Cuit:',
                'nombres':'Nombres:', 'apellidos':'Apellidos:',
                'direccion':'Dirección:', 'localidad':'Localidad:',
                'celular':'Celular:', 'telefono':'Teléfono:',
                'email':'Email:', 'tipoDeCliente':'Tipo de Cliente:',
                'descuentoServicio': 'Descuento Servicio:',
                'descuentoProducto': 'Descuento Producto:',
                'cuentaCorriente' : 'Cuenta Corriente:', 'baja':'Baja:'
            }

            error_messages = {
                'nombres' : {
                    'max_length': ("Nombres demasiados largos"),
                },

                'apellidos' : {
                    'max_length' : ("Apellidos demasiados largos"),
                },

                'dniCuit' : {
                    'max_length' : ("DNI/CUIT demasiado largo"),
                    'unique' : ("Ese DNI/CUIT ya existe"),
                },

                'descuentoServicio': {
                    'max_digits': "Debe ingresar a lo sumo %d digitos para la parte entera" % (Cliente.DESC_PARTE_ENTERA),
                    'max_whole_digits': "Debe ingresar a lo sumo %d digitos en total" % (Cliente.DESCUENTO),
                    'max_decimal_places': "Debe ingresar a lo sumo %d digitos para la parte decimal" % (Cliente.PARTE_DECIMAL),
                },

                'descuentoProducto': {
                    'max_digits': "Debe ingresar a lo sumo %d digitos para la parte entera" % (Cliente.DESC_PARTE_ENTERA),
                    'max_whole_digits': "Debe ingresar a lo sumo %d digitos en total" % (Cliente.DESCUENTO),
                },

            }

            widgets = {
                'localidad' : forms.Select(choices=Cliente.LOCALIDADES),
                'descuentoServicio': forms.NumberInput(attrs={'data-tipo': 'especial'}),
                'descuentoProducto': forms.NumberInput(attrs={'data-tipo': 'especial'}),
                'cuentaCorriente': forms.NumberInput(attrs={'data-tipo': 'especial'})
            }

        def clean_dniCuit(self):
            dato = self.data["dniCuit"]
            try:
                return lforms.ARDNIField().clean(dato)
            except forms.ValidationError:
                pass
            return lforms.ARCUITField().clean(dato)

        def clean(self):
            cleaned_data = super().clean()
            return cleaned_data

        def __init__(self, *args, **kwargs):

            super().__init__(*args, **kwargs)

            # [TODO] Averiguar una mejor manera de hacer esto:
            for field in self.fields.values():
                if not isinstance(field.widget, forms.CheckboxInput):
                    field.widget.attrs.update({
                        'class': 'form-control'
                    })

    return ClienteForm

class FiltradoForm(forms.Form):

    ordenes = (
        ("d", "Descendente"),
        ("a", "Ascendente"),
    )

    criterios = (
        ("dniCuit", "DNI/CUIT"),
        ("nombres", "Nombres"),
        ("apellidos", "Apellidos"),
        ("localidad", "Localiad"),
        ("tipoDeCliente", "TipoDeCliente"),
    )

    dniCuit = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder":"DNI/CUIT...",
            "class":"form-control"
        })
    )

    apellidos = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder":"Apellidos...",
            "class":"form-control",
        })
    )

    nombres = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder":"Nombres...",
            "class":"form-control"
        })
    )

    localidad = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder":"Localidad...",
            "class":"form-control",
        })
    )

    tipoDeCliente = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder":"Tipo De Cliente...",
            "class":"form-control",
        })
    )

    def filtros(self):
        retorno = {}
        if self.is_valid():

            fields = ("dniCuit", "apellidos", "nombres", "localidad", "tipoDeCliente")
            for field in fields:
                    if field in self.cleaned_data and self.cleaned_data[field]:
                        retorno[field] = self.cleaned_data[field]
        
        return retorno

    def criterio(self):
        if self.cleaned_data and "segun" in self.cleaned_data:
            return self.cleaned_data["segun"]
        return None

    def ascendente(self):
        if self.cleaned_data and "orden" in self.cleaned_data:
            return (self.cleaned_data["orden"] == "a")
        return None
