# Generated by Django 2.0.8 on 2019-12-19 15:21

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dniCuit', models.CharField(error_messages={'blank': 'El dni/cuit es obligatorio', 'max_length': 'El dni/cuit puede tener a lo sumo 14 caracteres', 'unique': 'El dni/cuit ingresado ya existe'}, help_text='Dni/Cuit del Cliente', max_length=14, unique=True)),
                ('nombres', models.CharField(error_messages={'blank': 'El nombre es obligatorio', 'max_length': 'El nombre puede tener a lo sumo 50 caracteres'}, help_text='Nombre del Cliente', max_length=50, validators=[django.core.validators.RegexValidator(regex='^[0-9a-zA-Z-_ .]{3,100}$')])),
                ('apellidos', models.CharField(blank=True, error_messages={'max_length': 'El apellido puede tener a lo sumo 50 caracteres'}, help_text='Apellido del Cliente', max_length=50, null=True, validators=[django.core.validators.RegexValidator(regex='^[0-9a-zA-Z-_ .]{3,100}$')])),
                ('direccion', models.CharField(error_messages={'max_length': 'El direccion puede tener a lo sumo 100 caracteres'}, help_text='Direccion del Cliente', max_length=100)),
                ('localidad', models.CharField(error_messages={'max_length': 'La localidad puede tener a lo sumo 60 caracteres'}, help_text='Localidad del Cliente', max_length=60)),
                ('celular', models.CharField(blank=True, error_messages={'max_length': 'El celular puede tener a lo sumo 12 caracteres', 'unique': 'Otro cliente tiene ese celular'}, help_text='Celular del Cliente sin el 0', max_length=12, null=True, unique=True, validators=[django.core.validators.RegexValidator(regex='^[0-9]{1,12}$')])),
                ('telefono', models.CharField(blank=True, error_messages={'max_length': 'El telefono puede tener a lo sumo 7 caracteres'}, help_text='Telefono del Cliente', max_length=7, null=True, validators=[django.core.validators.RegexValidator(regex='^[0-9]{1,12}$')])),
                ('email', models.EmailField(blank=True, error_messages={'unique': 'Otro cliente tiene ese email'}, help_text='Email del Cliente', max_length=254, null=True, unique=True)),
                ('tipoDeCliente', models.CharField(choices=[('C', 'Comun'), ('E', 'Especial')], default='C', error_messages={'blank': 'El tipo de cliente es obligatorio'}, help_text='Seleccione el tipo de cliente', max_length=1)),
                ('descuentoServicio', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), help_text='Los clientes especiales pueden tener un descuento en los serivios', max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0'), message='El descuento no puede ser menor a 0.00'), django.core.validators.MaxValueValidator(Decimal('100'), message='El descuento no puede ser mayor a 100.00')])),
                ('descuentoProducto', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), help_text='Los clientes especiales pueden tener un descuento en los productos que compren', max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0'), message='El descuento no puede ser menor a 0.00'), django.core.validators.MaxValueValidator(Decimal('100'), message='El descuento no puede ser mayor a 100.00')])),
                ('cuentaCorriente', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0'), message='El precio no debe ser menor a $0.00'), django.core.validators.MaxValueValidator(Decimal('3000'), message='El precio no puede ser mayor a $3000.00')])),
                ('baja', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['apellidos', 'nombres'],
                'verbose_name': 'Cliente',
                'permissions': (('cliente_crear', 'crear'), ('cliente_modificar', 'modificar'), ('cliente_eliminar', 'eliminar'), ('cliente_ver_habilitados', 'ver_habilitados'), ('cliente_listar_habilitados', 'listar_habilitados'), ('cliente_ver_no_habilitados', 'ver_no_habilitados'), ('cliente_listar_no_habilitados', 'listar_no_habilitados'), ('cliente_exportar_excel_habilitados', 'exportar_habilitados_excel'), ('cliente_exportar_excel_deshabilitados', 'exportar_deshabilitados_excel')),
                'verbose_name_plural': 'Clientes',
                'default_permissions': (),
            },
        ),
    ]
