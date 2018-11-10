# Generated by Django 2.0.9 on 2018-11-10 01:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rubro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(error_messages={'blank': 'El nombre es obligatorio', 'max_length': 'El nombre puede tener a lo sumo 50 caracteres'}, help_text='Nombre del Rubro', max_length=50, unique=True, validators=[django.core.validators.RegexValidator(regex='^[0-9a-zA-Z-_ .]{3,100}$')])),
                ('descripcion', models.TextField(blank=True, error_messages={'max_length': 'La descripcion puede tener a lo sumo 50 caracteres'}, help_text='Descripcion del Rubro', max_length=150, null=True)),
                ('baja', models.BooleanField(default=False)),
            ],
        ),
    ]
