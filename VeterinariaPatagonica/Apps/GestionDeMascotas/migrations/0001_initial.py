# Generated by Django 2.1.dev20180423170307 on 2019-12-20 12:29

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('GestionDeClientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mascota',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patente', models.CharField(blank=True, error_messages={'blank': 'la patente es obligatoria', 'max_length': 'la patente puede tener a lo sumo 6 caracteres', 'unique': 'Otra mascota tiene esa patente'}, help_text='patente la mascota', max_length=6, unique=True)),
                ('nombre', models.CharField(error_messages={'blank': 'El nombre es obligatorio', 'max_length': 'El nombre puede tener a lo sumo 50 caracteres'}, help_text='Nombre de la mascota', max_length=50, validators=[django.core.validators.RegexValidator(regex='^[0-9a-zA-Z-_ .]{3,100}$')])),
                ('fechaNacimiento', models.DateField(default=datetime.datetime.now, error_messages={'required': 'la fecha es obligatorio'}, help_text='Fecha de nacimiento de la mascota')),
                ('especie', models.CharField(error_messages={'blank': 'La especie es obligatorio', 'max_length': 'La especie puede tener a lo sumo 50 caracteres'}, help_text='Especie de la Mascota', max_length=50, validators=[django.core.validators.RegexValidator(regex='^[0-9a-zA-Z-_ .]{3,100}$')])),
                ('raza', models.CharField(error_messages={'blank': 'La especie es obligatorio', 'max_length': 'La especie puede tener a lo sumo 50 caracteres'}, help_text='Especie de la Mascota', max_length=50, validators=[django.core.validators.RegexValidator(regex='^[0-9a-zA-Z-_ .]{3,100}$')])),
                ('baja', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(error_messages={}, help_text='Ingrese cliente', on_delete=django.db.models.deletion.CASCADE, to='GestionDeClientes.Cliente')),
            ],
            options={
                'ordering': ['patente'],
                'permissions': (('mascota_crear', 'crear'), ('mascota_modificar', 'modificar'), ('mascota_eliminar', 'eliminar'), ('mascota_ver_habilitados', 'ver_habilitados'), ('mascota_listar_habilitados', 'listar_habilitados'), ('mascota_ver_no_habilitados', 'ver_no_habilitados'), ('mascota_listar_no_habilitados', 'listar_no_habilitados'), ('deshabilitar_mascota', 'deshabilitar_mascota')),
                'default_permissions': (),
            },
        ),
    ]
