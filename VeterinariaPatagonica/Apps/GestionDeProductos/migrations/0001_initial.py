# Generated by Django 2.1.dev20180423170307 on 2019-12-20 12:28

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('GestionDeRubros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(error_messages={'blank': 'El nombre es obligatorio', 'max_length': 'El nombre puede tener a lo sumo 50 caracteres'}, help_text='Nombre del Producto / Insumo', max_length=50, validators=[django.core.validators.RegexValidator(regex='^[0-9a-zA-Z-_ .]{3,100}$')])),
                ('marca', models.CharField(error_messages={'blank': 'La marca es obligatoria', 'max_length': 'La marca puede tener a lo sumo 50 caracteres'}, help_text='Marca del Producto / Insumo', max_length=50, validators=[django.core.validators.RegexValidator(regex='^[0-9a-zA-Z-_ .]{3,100}$')])),
                ('stock', models.IntegerField(help_text='Stock del Producto / Insumo', validators=[django.core.validators.MinValueValidator(0, message='El Stock no puede ser menor a 0')])),
                ('formaDePresentacion', models.PositiveSmallIntegerField(choices=[(1, 'g'), (2, 'cm3'), (3, 'unidad'), (4, 'kg'), (5, 'litro'), (6, 'docena')], error_messages={'blank': 'La unidad de medida es obligatoria', 'invalid_choice': 'Opcion invalida'}, help_text='Forma de Presentacion del Producto / Insumo')),
                ('precioPorUnidad', models.DecimalField(decimal_places=2, help_text='Precio del Producto / Insumo', max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0'), message='El precio no debe ser menor a $0.00'), django.core.validators.MaxValueValidator(Decimal('9000'), message='El precio no puede ser mayor a $9000.00')])),
                ('precioDeCompra', models.DecimalField(decimal_places=2, help_text='Precio de Compra del Producto / Insumo', max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0'), message='El precio no debe ser menor a $0.00'), django.core.validators.MaxValueValidator(Decimal('9000'), message='El precio no puede ser mayor a $9000.00')])),
                ('descripcion', models.TextField(blank=True, error_messages={'max_length': 'La descripcion puede tener a lo sumo 150 caracteres'}, help_text='Descripcion del Producto / Insumo', max_length=150, null=True)),
                ('baja', models.BooleanField(default=False)),
                ('rubro', models.ForeignKey(error_messages={'blank': 'El rubro es obligatorio'}, help_text='Nombre del rubro', on_delete=django.db.models.deletion.CASCADE, to='GestionDeRubros.Rubro')),
            ],
            options={
                'ordering': ['nombre', 'marca'],
                'permissions': (('producto_crear', 'crear'), ('producto_modificar', 'modificar'), ('producto_eliminar', 'eliminar'), ('producto_ver_habilitados', 'ver_habilitados'), ('producto_listar_habilitados', 'listar_habilitados'), ('producto_ver_no_habilitados', 'ver_no_habilitados'), ('producto_listar_no_habilitados', 'listar_no_habilitados'), ('deshabilitar_producto', 'deshabilitar_producto')),
                'default_permissions': (),
            },
        ),
    ]
