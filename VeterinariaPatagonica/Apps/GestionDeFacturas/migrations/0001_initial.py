# Generated by Django 2.1.dev20180423170307 on 2019-12-20 12:29

import datetime
from decimal import Decimal
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
            name='DetalleFactura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], default='B', error_messages={'blank': 'El tipo es obligatorio', 'max_length': 'El tipo de factura puede tener a lo sumo 1 caracteres'}, help_text='Tipo de Factura.', max_length=1, validators=[django.core.validators.RegexValidator(regex='^[A-B-C]{1}$')])),
                ('fecha', models.DateField(default=datetime.datetime.now, error_messages={'blank': 'La fecha es obligatoria'}, help_text='Fecha de la Factura.')),
                ('recargo', models.DecimalField(decimal_places=2, default=Decimal('0'), error_messages={}, max_digits=5)),
                ('descuento', models.DecimalField(decimal_places=2, default=Decimal('0'), error_messages={}, max_digits=5)),
                ('total', models.DecimalField(decimal_places=2, default=Decimal('0'), error_messages={}, max_digits=8, validators=[django.core.validators.MinValueValidator(0, 'El precio de la factura no puede ser negativo')])),
                ('cliente', models.ForeignKey(error_messages={'blank': 'El cliente es obligatorio'}, on_delete=django.db.models.deletion.CASCADE, to='GestionDeClientes.Cliente')),
            ],
            options={
                'ordering': ['-fecha', 'tipo'],
                'permissions': (('factura_crear', 'crear'), ('factura_ver_pagas', 'ver'), ('factura_ver_no_pagas', 'ver'), ('factura_listar_pagas', 'listar pagas'), ('factura_listar_no_pagas', 'listar no pagas'), ('factura_exportar_xlsx_pagas', 'exportar a formato xlsx pagas'), ('factura_exportar_xlsx_no_pagas', 'exportar a formato xlsx no pagas')),
                'default_permissions': (),
            },
        ),
    ]
