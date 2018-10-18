from django import forms
from .models import Mascota

from django.core.validators import RegexValidator

#from localflavor.ar import forms as lforms

from localflavor.ar import forms as lforms


#TIMEINPUT_FMTS = [ "%H:%M" ]


'''class creacionModelForm(forms.ModelForm):
    class meta:
        model = Mascota'''

def MascotaFormFactory(mascota=None):
    campos = [ 'nombre',
               'raza',
               'especie']
    if mascota is  None:
        campos.insert(0, 'patente')


    class MascotaForm(forms.ModelForm):
        class Meta:
            model = Mascota
            fields = campos
            labels = {
                'patente':'Patente',
                'nombre':'Nombre',
                'fechaDeNacimiento' : 'FechaDeNacimiento',
                'cliente': "Cliente",
                'raza':'Raza',
                'especie':'Especie',
                'baja':'Baja'
            }
            error_messages = {
                'nombre' : {
                    'max_length': ("Nombre demasiados largos"),
                },
                'patente' : {
                    #'max_length' : ("patente demasiado largo"),
                    'unique' : ("Esa patente ya existe"),
                }
            }
            widgets = {
                'nombre' : forms.TextInput(),
                'raza' : forms.TextInput(),
                'cliente': forms.Select(attrs={'class':'form-control'}),
                'especie': forms.TextInput(),

            }

        def clean_patente(self):
            dato = self.data["patente"]
            try:
                return lforms.ARDNIField().clean(dato)
            except forms.ValidationError:
                pass

            return lforms.ARCUITField().clean(dato)

        def clean(self):
            cleaned_data = super().clean()
            return cleaned_data
    return MascotaForm