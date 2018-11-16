# Generated by Django 2.0.8 on 2018-11-12 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('GestionDeServicios', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('GestionDeProductos', '0001_initial'),
        ('GestionDePracticas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='estado',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='realizadaservicio',
            name='realizada',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='realizada_servicios', to='GestionDePracticas.Realizada'),
        ),
        migrations.AddField(
            model_name='realizadaproducto',
            name='realizada',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='realizada_productos', to='GestionDePracticas.Realizada'),
        ),
        migrations.AddField(
            model_name='realizada',
            name='productos',
            field=models.ManyToManyField(related_name='realizadas', through='GestionDePracticas.RealizadaProducto', to='GestionDeProductos.Producto'),
        ),
        migrations.AddField(
            model_name='realizada',
            name='servicios',
            field=models.ManyToManyField(related_name='realizadas', through='GestionDePracticas.RealizadaServicio', to='GestionDeServicios.Servicio'),
        ),
        migrations.AlterUniqueTogether(
            name='practicaservicio',
            unique_together={('practica', 'servicio')},
        ),
        migrations.AlterIndexTogether(
            name='practicaservicio',
            index_together={('practica', 'servicio')},
        ),
        migrations.AlterUniqueTogether(
            name='practicaproducto',
            unique_together={('practica', 'producto')},
        ),
        migrations.AlterIndexTogether(
            name='practicaproducto',
            index_together={('practica', 'producto')},
        ),
        migrations.AlterUniqueTogether(
            name='realizadaservicio',
            unique_together={('realizada', 'servicio')},
        ),
        migrations.AlterIndexTogether(
            name='realizadaservicio',
            index_together={('realizada', 'servicio')},
        ),
        migrations.AlterUniqueTogether(
            name='realizadaproducto',
            unique_together={('realizada', 'producto')},
        ),
        migrations.AlterIndexTogether(
            name='realizadaproducto',
            index_together={('realizada', 'producto')},
        ),
    ]
