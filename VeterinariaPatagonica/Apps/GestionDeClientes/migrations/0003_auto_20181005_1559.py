# Generated by Django 2.0.8 on 2018-10-05 18:59

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('GestionDeClientes', '0002_cliente_celular'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='DNI_CUIT',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='id',
        ),
        migrations.AddField(
            model_name='cliente',
            name='dniCuit',
            field=models.CharField(default=django.utils.timezone.now, error_messages={'blank': 'El dni/cuit es obligatorio', 'max_length': 'El dni/cuit puede tener a lo sumo 14 caracteres', 'unique': 'Otro cliente tiene ese dni/cuit'}, help_text='Dni/Cuit del Cliente', max_length=14, primary_key=True, serialize=False, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='apellidos',
            field=models.CharField(blank=True, error_messages={'max_length': 'El apellido puede tener a lo sumo 50 caracteres'}, help_text='Apellido del Cliente', max_length=50, null=True, validators=[django.core.validators.RegexValidator(regex='^[0-9a-zA-Z-_ .]{3,100}$')]),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='celular',
            field=models.CharField(blank=True, error_messages={'max_length': 'El celular puede tener a lo sumo 10 caracteres', 'unique': 'Otro cliente tiene ese celular'}, help_text='Celular del Cliente sin el 0', max_length=10, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='direccion',
            field=models.CharField(error_messages={'max_length': 'El direccion puede tener a lo sumo 100 caracteres'}, help_text='Direccion del Cliente', max_length=100),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.EmailField(blank=True, error_messages={'unique': 'Otro cliente tiene ese email'}, help_text='Email del Cliente', max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='localidad',
            field=models.CharField(error_messages={'max_length': 'La localidad puede tener a lo sumo 60 caracteres'}, help_text='Localidad del Cliente', max_length=60),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nombres',
            field=models.CharField(error_messages={'blank': 'El nombre es obligatorio', 'max_length': 'El nombre puede tener a lo sumo 50 caracteres'}, help_text='Nombre del Cliente', max_length=50, validators=[django.core.validators.RegexValidator(regex='^[0-9a-zA-Z-_ .]{3,100}$')]),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(blank=True, error_messages={'max_length': 'El telefono puede tener a lo sumo 7 caracteres'}, help_text='Telefono del Cliente', max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='tipoDeCliente',
            field=models.CharField(choices=[('E', 'Especial'), ('C', 'Comun')], default='C', error_messages={'blank': 'El tipo de cliente es obligatorio'}, max_length=1),
        ),
    ]
