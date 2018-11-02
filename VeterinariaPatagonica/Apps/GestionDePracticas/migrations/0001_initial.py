# Generated by Django 2.0.9 on 2018-11-02 03:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('GestionDeMascotas', '0001_initial'),
        ('GestionDeServicios', '0001_initial'),
        ('GestionDeProductos', '0001_initial'),
        ('GestionDeClientes', '0001_initial'),
        ('GestionDeTiposDeAtencion', '0002_auto_20181102_0025'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.DateTimeField(auto_now=True)),
                ('tipo', models.PositiveSmallIntegerField(choices=[(0, 'estado'), (1, 'creada'), (2, 'programada'), (3, 'presupuestada'), (4, 'cancelada'), (5, 'realizada'), (6, 'facturada')])),
            ],
            options={
                'get_latest_by': 'marca',
            },
        ),
        migrations.CreateModel(
            name='Practica',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(error_messages={'blank': 'El nombre es obligatorio.', 'max_length': 'El nombre puede tener a lo sumo 100 caracteres.', 'unique': 'Otra práctica tiene ese nombre.'}, max_length=100, unique=True)),
                ('precio', models.DecimalField(decimal_places=2, error_messages={'max_digits': 'Cantidad de digitos ingresados supera el máximo.'}, max_digits=8)),
                ('montoAbonado', models.DecimalField(decimal_places=2, error_messages={'max_digits': 'Cantidad de digitos ingresados supera el máximo.'}, max_digits=8)),
                ('cliente', models.ForeignKey(error_messages={}, on_delete=django.db.models.deletion.CASCADE, to='GestionDeClientes.Cliente')),
                ('mascota', models.ForeignKey(error_messages={}, on_delete=django.db.models.deletion.CASCADE, to='GestionDeMascotas.Mascota')),
            ],
        ),
        migrations.CreateModel(
            name='PracticaProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('practica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionDePracticas.Practica')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionDeProductos.Producto')),
            ],
        ),
        migrations.CreateModel(
            name='PracticaServicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('practica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionDePracticas.Practica')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionDeServicios.Servicio')),
            ],
        ),
        migrations.CreateModel(
            name='Cancelada',
            fields=[
                ('estado_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='GestionDePracticas.Estado')),
            ],
            bases=('GestionDePracticas.estado',),
        ),
        migrations.CreateModel(
            name='Creada',
            fields=[
                ('estado_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='GestionDePracticas.Estado')),
            ],
            bases=('GestionDePracticas.estado',),
        ),
        migrations.CreateModel(
            name='Facturada',
            fields=[
                ('estado_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='GestionDePracticas.Estado')),
            ],
            bases=('GestionDePracticas.estado',),
        ),
        migrations.CreateModel(
            name='Presupuestada',
            fields=[
                ('estado_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='GestionDePracticas.Estado')),
                ('porcentajeDescuento', models.PositiveSmallIntegerField()),
                ('diasMantenimiento', models.PositiveSmallIntegerField()),
            ],
            bases=('GestionDePracticas.estado',),
        ),
        migrations.CreateModel(
            name='Programada',
            fields=[
                ('estado_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='GestionDePracticas.Estado')),
                ('turno', models.DateTimeField(auto_now=True)),
                ('motivoReprogramacion', models.CharField(max_length=100)),
                ('senia', models.PositiveSmallIntegerField()),
            ],
            bases=('GestionDePracticas.estado',),
        ),
        migrations.CreateModel(
            name='Realizada',
            fields=[
                ('estado_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='GestionDePracticas.Estado')),
            ],
            bases=('GestionDePracticas.estado',),
        ),
        migrations.AddField(
            model_name='practica',
            name='productosReales',
            field=models.ManyToManyField(through='GestionDePracticas.PracticaProducto', to='GestionDeProductos.Producto'),
        ),
        migrations.AddField(
            model_name='practica',
            name='servicios',
            field=models.ManyToManyField(through='GestionDePracticas.PracticaServicio', to='GestionDeServicios.Servicio'),
        ),
        migrations.AddField(
            model_name='practica',
            name='tipoDeAtencion',
            field=models.ForeignKey(error_messages={}, on_delete=django.db.models.deletion.CASCADE, to='GestionDeTiposDeAtencion.TipoDeAtencion'),
        ),
        migrations.AddField(
            model_name='estado',
            name='practica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estados', to='GestionDePracticas.Practica'),
        ),
        migrations.AddField(
            model_name='estado',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
