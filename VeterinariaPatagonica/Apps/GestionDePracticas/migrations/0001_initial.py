# Generated by Django 2.0.8 on 2019-12-20 09:36

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('GestionDeTiposDeAtencion', '0001_initial'),
        ('GestionDeProductos', '0001_initial'),
        ('GestionDeClientes', '0001_initial'),
        ('GestionDeMascotas', '0001_initial'),
        ('GestionDeServicios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adelanto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('importe', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=8, validators=[django.core.validators.MinValueValidator(0, 'El importe del adelanto no puede ser negativo')])),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.DateTimeField(auto_now_add=True)),
                ('tipo', models.PositiveSmallIntegerField(choices=[(0, 'estado'), (1, 'creada'), (3, 'presupuestada'), (2, 'programada'), (5, 'realizada'), (6, 'facturada'), (4, 'cancelada')])),
            ],
            options={
                'get_latest_by': 'marca',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Practica',
            fields=[
                ('tipo', models.CharField(choices=[('C', 'Consulta'), ('Q', 'Cirugia')], editable=False, max_length=1)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('precio', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(0, 'El precio de la practica no puede ser negativo')])),
                ('adelanto', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='practica', to='GestionDePracticas.Adelanto')),
                ('cliente', models.ForeignKey(error_messages={'blank': 'El cliente es obligatorio', 'null': 'El cliente no puede ser null'}, on_delete=django.db.models.deletion.CASCADE, related_name='practicas', to='GestionDeClientes.Cliente')),
                ('mascota', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='practicas', to='GestionDeMascotas.Mascota')),
            ],
            options={
                'permissions': (('crear_consulta_atendida', 'Permiso para crear consultas'), ('crear_cirugia_atendida', 'Permiso para crear cirugias'), ('listar_consulta_atendida', 'Permiso para listar consultas'), ('listar_cirugia_atendida', 'Permiso para listar cirugias'), ('listar_consulta_no_atendida', 'Permiso para listar consultas atendidas por otro usuario'), ('listar_cirugia_no_atendida', 'Permiso para listar cirugias atendidas por otro usuario'), ('ver_informacion_general_consulta_atendida', 'Permiso para ver informacion general de consultas'), ('ver_informacion_general_consulta_no_atendida', 'Permiso para ver informacion general de consultas atendidas por otro usuario'), ('ver_informacion_general_cirugia_atendida', 'Permiso para ver informacion general de cirugias'), ('ver_informacion_general_cirugia_no_atendida', 'Permiso para ver informacion general de cirugias atendidas por otro usuario'), ('ver_informacion_clinica_consulta_atendida', 'Permiso para ver informacion clinica de consultas'), ('ver_informacion_clinica_consulta_no_atendida', 'Permiso para ver informacion clinica de consultas atendidas por otro usuario'), ('ver_informacion_clinica_cirugia_atendida', 'Permiso para ver informacion clinica de cirugias'), ('ver_informacion_clinica_cirugia_no_atendida', 'Permiso para ver informacion clinica de cirugias atendidas por otro usuario'), ('ver_detalle_estado_consulta_atendida', 'Permiso para ver informacion detallada de consultas'), ('ver_detalle_estado_consulta_no_atendida', 'Permiso para ver informacion detallada de consultas atendidas por otro usuario'), ('ver_detalle_estado_cirugia_atendida', 'Permiso para ver informacion detallada de cirugias'), ('ver_detalle_estado_cirugia_no_atendida', 'Permiso para ver informacion detallada de cirugias atendidas por otro usuario'), ('ver_reporte_consulta', 'Permiso para ver reporte de consultas'), ('ver_reporte_cirugia', 'Permiso para ver reporte de cirugias'), ('exportar_xlsx_consulta_atendida', 'Permiso para exportar en xlsx consultas'), ('exportar_xlsx_consulta_no_atendida', 'Permiso para exportar en xlsx consultas atendidas por otro usuario'), ('exportar_xlsx_cirugia_atendida', 'Permiso para exportar en xlsx cirugias'), ('exportar_xlsx_cirugia_no_atendida', 'Permiso para exportar en xlsx cirugias atendidas por otro usuario')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='PracticaProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'La cantidad debe ser mayor que cero')])),
                ('precio', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0'), message='El precio no puede ser menor a 0.00')])),
                ('practica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='practica_productos', to='GestionDePracticas.Practica')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producto_practicas', to='GestionDeProductos.Producto')),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='PracticaServicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'La cantidad debe ser mayor que cero')])),
                ('precio', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0'), message='El precio no puede ser menor a 0.00')])),
                ('practica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='practica_servicios', to='GestionDePracticas.Practica')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicio_practicas', to='GestionDeServicios.Servicio')),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='RealizadaProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'La cantidad debe ser mayor que cero')])),
                ('precio', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0'), message='El precio no puede ser menor a 0.00')])),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producto_realizadas', to='GestionDeProductos.Producto')),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='RealizadaServicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'La cantidad debe ser mayor que cero')])),
                ('precio', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0'), message='El precio no puede ser menor a 0.00')])),
                ('observaciones', models.TextField(blank=True)),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicio_realizadas', to='GestionDeServicios.Servicio')),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Cancelada',
            fields=[
                ('estado_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='GestionDePracticas.Estado')),
                ('motivo', models.TextField(blank=True)),
            ],
            options={
                'permissions': (('listar_cirugia_cancelada_atendida', 'Permiso para listar cirugias en estado cancelada'), ('listar_cirugia_cancelada_no_atendida', 'Permiso para listar cirugias en estado cancelada atendidas por otro usuario'), ('ver_detalle_estado_cirugia_cancelada_atendida', 'Permiso para ver informacion detallada de cirugias en estado cancelada'), ('ver_detalle_estado_cirugia_cancelada_no_atendida', 'Permiso para ver informacion detallada de cirugias en estado cancelada atendidas por otro usuario'), ('exportar_xlsx_consulta_cancelada_atendida', 'Permiso para exportar en xlsx consultas canceladas'), ('exportar_xlsx_consulta_cancelada_no_atendida', 'Permiso para exportar en xlsx consultas canceladas atendidas por otro usuario'), ('exportar_xlsx_cirugia_cancelada_atendida', 'Permiso para exportar en xlsx cirugias canceladas'), ('exportar_xlsx_cirugia_cancelada_no_atendida', 'Permiso para exportar en xlsx cirugias canceladas atendidas por otro usuario')),
                'default_permissions': (),
            },
            bases=('GestionDePracticas.estado',),
        ),
        migrations.CreateModel(
            name='Creada',
            fields=[
                ('estado_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='GestionDePracticas.Estado')),
            ],
            options={
                'permissions': (('presupuestar_consulta_creada_atendida', 'Permiso para presupuestar consultas en estado creada'), ('presupuestar_cirugia_creada_atendida', 'Permiso para presupuestar cirugias en estado creada'), ('programar_cirugia_creada_atendida', 'Permiso para programar cirugias en estado creada'), ('realizar_consulta_creada_atendida', 'Permiso para realizar consultas en estado creada'), ('realizar_cirugia_creada_atendida', 'Permiso para realizar cirugias en estado creada'), ('presupuestar_consulta_creada_no_atendida', 'Permiso para presupuestar consultas en estado creada atendidas por otro usuario'), ('presupuestar_cirugia_creada_no_atendida', 'Permiso para presupuestar cirugias en estado creada atendidas por otro usuario'), ('programar_cirugia_creada_no_atendida', 'Permiso para programar cirugias en estado creada atendidas por otro usuario'), ('realizar_consulta_creada_no_atendida', 'Permiso para realizar consultas en estado creada atendidas por otro usuario'), ('realizar_cirugia_creada_no_atendida', 'Permiso para realizar cirugias en estado creada atendidas por otro usuario'), ('exportar_xlsx_consulta_creada_atendida', 'Permiso para exportar en xlsx consultas creadas'), ('exportar_xlsx_consulta_creada_no_atendida', 'Permiso para exportar en xlsx consultas creadas atendidas por otro usuario'), ('exportar_xlsx_cirugia_creada_atendida', 'Permiso para exportar en xlsx cirugias creadas'), ('exportar_xlsx_cirugia_creada_no_atendida', 'Permiso para exportar en xlsx cirugias creadas atendidas por otro usuario')),
                'default_permissions': (),
            },
            bases=('GestionDePracticas.estado',),
        ),
        migrations.CreateModel(
            name='Facturada',
            fields=[
                ('estado_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='GestionDePracticas.Estado')),
            ],
            options={
                'permissions': (('listar_consulta_facturada_atendida', 'Permiso para listar consultas en estado facturada'), ('listar_consulta_facturada_no_atendida', 'Permiso para listar consultas en estado facturada atendidas por otro usuario'), ('listar_cirugia_facturada_atendida', 'Permiso para listar cirugias en estado facturada'), ('listar_cirugia_facturada_no_atendida', 'Permiso para listar cirugias en estado facturada atendidas por otro usuario'), ('ver_detalle_estado_consulta_facturada_atendida', 'Permiso para ver informacion detallada de consultas en estado facturada'), ('ver_detalle_estado_consulta_facturada_no_atendida', 'Permiso para ver informacion detallada de consultas en estado facturada atendidas por otro usuario'), ('ver_detalle_estado_cirugia_facturada_atendida', 'Permiso para ver informacion detallada de cirugias en estado facturada'), ('ver_detalle_estado_cirugia_facturada_no_atendida', 'Permiso para ver informacion detallada de cirugias en estado facturada atendidas por otro usuario'), ('ver_informacion_clinica_consulta_facturada_atendida', 'Permiso para ver informacion clinica de consultas'), ('ver_informacion_clinica_consulta_facturada_no_atendida', 'Permiso para ver informacion clinica de consultas atendidas por otro usuario'), ('ver_informacion_clinica_cirugia_facturada_atendida', 'Permiso para ver informacion clinica de cirugias'), ('ver_informacion_clinica_cirugia_facturada_no_atendida', 'Permiso para ver informacion clinica de cirugias atendidas por otro usuario'), ('exportar_xlsx_consulta_facturada_atendida', 'Permiso para exportar en xlsx consultas facturadas'), ('exportar_xlsx_consulta_facturada_no_atendida', 'Permiso para exportar en xlsx consultas facturadas atendidas por otro usuario'), ('exportar_xlsx_cirugia_facturada_atendida', 'Permiso para exportar en xlsx cirugias facturadas'), ('exportar_xlsx_cirugia_facturada_no_atendida', 'Permiso para exportar en xlsx cirugias facturadas atendidas por otro usuario')),
                'default_permissions': (),
            },
            bases=('GestionDePracticas.estado',),
        ),
        migrations.CreateModel(
            name='Presupuestada',
            fields=[
                ('estado_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='GestionDePracticas.Estado')),
                ('diasMantenimiento', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Los dias de mantenimiento del presupuesto deben ser mas que cero')])),
            ],
            options={
                'permissions': (('realizar_consulta_presupuestada_atendida', 'Permiso para realizar consultas en estado presupuestada'), ('realizar_consulta_presupuestada_no_atendida', 'Permiso para realizar consultas en estado presupuestada atendidas por otro usuario'), ('realizar_cirugia_presupuestada_atendida', 'Permiso para realizar cirugias en estado presupuestada'), ('realizar_cirugia_presupuestada_no_atendida', 'Permiso para realizar cirugias en estado presupuestada atendidas por otro usuario'), ('programar_cirugia_presupuestada_atendida', 'Permiso para programar cirugias en estado presupuestada'), ('programar_cirugia_presupuestada_no_atendida', 'Permiso para programar cirugias en estado presupuestada atendidas por otro usuario'), ('listar_consulta_presupuestada_atendida', 'Permiso para listar consultas en estado presupuestada'), ('listar_consulta_presupuestada_no_atendida', 'Permiso para listar consultas en estado presupuestada atendidas por otro usuario'), ('listar_cirugia_presupuestada_atendida', 'Permiso para listar cirugias en estado presupuestada'), ('listar_cirugia_presupuestada_no_atendida', 'Permiso para listar cirugias en estado presupuestada atendidas por otro usuario'), ('ver_detalle_estado_consulta_presupuestada_atendida', 'Permiso para ver informacion detallada de consultas en estado presupuestada'), ('ver_detalle_estado_consulta_presupuestada_no_atendida', 'Permiso para ver informacion detallada de consultas en estado presupuestada atendidas por otro usuario'), ('ver_detalle_estado_cirugia_presupuestada_atendida', 'Permiso para ver informacion detallada de cirugias en estado presupuestada'), ('ver_detalle_estado_cirugia_presupuestada_no_atendida', 'Permiso para ver informacion detallada de cirugias en estado presupuestada atendidas por otro usuario'), ('exportar_xlsx_consulta_presupuestada_atendida', 'Permiso para exportar en xlsx consultas presupuestadas'), ('exportar_xlsx_consulta_presupuestada_no_atendida', 'Permiso para exportar en xlsx consultas presupuestadas atendidas por otro usuario'), ('exportar_xlsx_cirugia_presupuestada_atendida', 'Permiso para exportar en xlsx cirugias presupuestadas'), ('exportar_xlsx_cirugia_presupuestada_no_atendida', 'Permiso para exportar en xlsx cirugias presupuestadas atendidas por otro usuario')),
                'default_permissions': (),
            },
            bases=('GestionDePracticas.estado',),
        ),
        migrations.CreateModel(
            name='Programada',
            fields=[
                ('estado_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='GestionDePracticas.Estado')),
                ('inicio', models.DateTimeField()),
                ('finalizacion', models.DateTimeField()),
                ('motivoReprogramacion', models.CharField(blank=True, max_length=300, verbose_name='Motivo de reprogramacion')),
            ],
            options={
                'permissions': (('reprogramar_cirugia_programada_atendida', 'Permiso para reprogramar cirugias en estado programada'), ('reprogramar_cirugia_programada_no_atendida', 'Permiso para reprogramar cirugias en estado programada atendidas por otro usuario'), ('realizar_cirugia_programada_atendida', 'Permiso para realizar cirugias en estado programada'), ('realizar_cirugia_programada_no_atendida', 'Permiso para realizar cirugias en estado programada atendidas por otro usuario'), ('cancelar_cirugia_programada_atendida', 'Permiso para cancelar cirugias en estado programada'), ('cancelar_cirugia_programada_no_atendida', 'Permiso para cancelar cirugias en estado programada atendidas por otro usuario'), ('listar_cirugia_programada_atendida', 'Permiso para listar cirugias en estado programada'), ('listar_cirugia_programada_no_atendida', 'Permiso para listar cirugias en estado programada atendidas por otro usuario'), ('ver_detalle_estado_cirugia_programada_atendida', 'Permiso para ver informacion detallada de cirugias en estado programada'), ('ver_detalle_estado_cirugia_programada_no_atendida', 'Permiso para ver informacion detallada de cirugias en estado programada atendidas por otro usuario'), ('exportar_xlsx_consulta_programada_atendida', 'Permiso para exportar en xlsx consultas programadas'), ('exportar_xlsx_consulta_programada_no_atendida', 'Permiso para exportar en xlsx consultas programadas atendidas por otro usuario'), ('exportar_xlsx_cirugia_programada_atendida', 'Permiso para exportar en xlsx cirugias programadas'), ('exportar_xlsx_cirugia_programada_no_atendida', 'Permiso para exportar en xlsx cirugias programadas atendidas por otro usuario')),
                'default_permissions': (),
            },
            bases=('GestionDePracticas.estado',),
        ),
        migrations.CreateModel(
            name='Realizada',
            fields=[
                ('estado_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='GestionDePracticas.Estado')),
                ('inicio', models.DateTimeField()),
                ('finalizacion', models.DateTimeField()),
                ('condicionPreviaMascota', models.TextField(blank=True)),
                ('resultados', models.TextField(blank=True)),
            ],
            options={
                'permissions': (('facturar_consulta_realizada_atendida', 'Permiso para facturar consultas en estado realizada'), ('facturar_consulta_realizada_no_atendida', 'Permiso para facturar consultas en estado realizada atendidas por otro usuario'), ('facturar_cirugia_realizada_atendida', 'Permiso para facturar cirugias en estado realizada'), ('facturar_cirugia_realizada_no_atendida', 'Permiso para facturar cirugias en estado realizada atendidas por otro usuario'), ('modificar_consulta_realizada_atendida', 'Permiso para modificar consultas en estado realizada'), ('modificar_consulta_realizada_no_atendida', 'Permiso para modificar consultas en estado realizada atendidas por otro usuario'), ('modificar_cirugia_realizada_atendida', 'Permiso para modificar cirugias en estado realizada'), ('modificar_cirugia_realizada_no_atendida', 'Permiso para modificar cirugias en estado realizada atendidas por otro usuario'), ('modificar_informacion_clinica_consulta_realizada_atendida', 'Permiso para modificar informacion clinica de consultas'), ('modificar_informacion_clinica_consulta_realizada_no_atendida', 'Permiso para modificar informacion clinica de consultas atendidas por otro usuario'), ('modificar_informacion_clinica_cirugia_realizada_atendida', 'Permiso para modificar informacion clinica de cirugias'), ('modificar_informacion_clinica_cirugia_realizada_no_atendida', 'Permiso para modificar informacion clinica de cirugias atendidas por otro usuario'), ('listar_consulta_realizada_atendida', 'Permiso para listar consultas en estado realizada'), ('listar_consulta_realizada_no_atendida', 'Permiso para listar consultas en estado realizada atendidas por otro usuario'), ('listar_cirugia_realizada_atendida', 'Permiso para listar cirugias en estado realizada'), ('listar_cirugia_realizada_no_atendida', 'Permiso para listar cirugias en estado realizada atendidas por otro usuario'), ('ver_informacion_clinica_consulta_realizada_atendida', 'Permiso para ver informacion clinica de consultas'), ('ver_informacion_clinica_consulta_realizada_no_atendida', 'Permiso para ver informacion clinica de consultas atendidas por otro usuario'), ('ver_informacion_clinica_cirugia_realizada_atendida', 'Permiso para ver informacion clinica de cirugias'), ('ver_informacion_clinica_cirugia_realizada_no_atendida', 'Permiso para ver informacion clinica de cirugias atendidas por otro usuario'), ('ver_detalle_estado_consulta_realizada_atendida', 'Permiso para ver informacion detallada de consultas en estado realizada'), ('ver_detalle_estado_consulta_realizada_no_atendida', 'Permiso para ver informacion detallada de consultas en estado realizada atendidas por otro usuario'), ('ver_detalle_estado_cirugia_realizada_atendida', 'Permiso para ver informacion detallada de cirugias en estado realizada'), ('ver_detalle_estado_cirugia_realizada_no_atendida', 'Permiso para ver informacion detallada de cirugias en estado realizada atendidas por otro usuario'), ('exportar_xlsx_consulta_realizada_atendida', 'Permiso para exportar en xlsx consultas realizadas'), ('exportar_xlsx_consulta_realizada_no_atendida', 'Permiso para exportar en xlsx consultas realizadas atendidas por otro usuario'), ('exportar_xlsx_cirugia_realizada_atendida', 'Permiso para exportar en xlsx cirugias realizadas'), ('exportar_xlsx_cirugia_realizada_no_atendida', 'Permiso para exportar en xlsx cirugias realizadas atendidas por otro usuario')),
                'default_permissions': (),
            },
            bases=('GestionDePracticas.estado',),
        ),
        migrations.AddField(
            model_name='practica',
            name='productos',
            field=models.ManyToManyField(related_name='practicas', related_query_name='practica', through='GestionDePracticas.PracticaProducto', to='GestionDeProductos.Producto'),
        ),
        migrations.AddField(
            model_name='practica',
            name='servicios',
            field=models.ManyToManyField(related_name='practicas', related_query_name='practica', through='GestionDePracticas.PracticaServicio', to='GestionDeServicios.Servicio'),
        ),
        migrations.AddField(
            model_name='practica',
            name='tipoDeAtencion',
            field=models.ForeignKey(error_messages={'blank': 'El tipo de atencion es obligatorio', 'null': 'El tipo de atencion no puede ser null'}, on_delete=django.db.models.deletion.CASCADE, related_name='practicas', to='GestionDeTiposDeAtencion.TipoDeAtencion'),
        ),
        migrations.AddField(
            model_name='estado',
            name='practica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estados', related_query_name='estado', to='GestionDePracticas.Practica'),
        ),
    ]
