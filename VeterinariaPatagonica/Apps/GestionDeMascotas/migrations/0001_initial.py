

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
                ('patente', models.CharField(error_messages={'blank': 'la patente es obligatoria', 'max_length': 'la patente puede tener a lo sumo 6 caracteres', 'unique': 'Otra mascota tiene esa patente'}, help_text='patente la mascota', max_length=6, unique=True)),
                ('nombre', models.CharField(error_messages={'blank': 'El nombre es obligatorio', 'max_length': 'El nombre puede tener a lo sumo 50 caracteres'}, help_text='Nombre de la mascota', max_length=50, validators=[django.core.validators.RegexValidator(regex='^[0-9a-zA-Z-_ .]{3,100}$')])),
                ('especie', models.CharField(error_messages={'blank': 'La especie es obligatorio', 'max_length': 'La especie puede tener a lo sumo 50 caracteres'}, help_text='Especie de la Mascota', max_length=50, validators=[django.core.validators.RegexValidator(regex='^[0-9a-zA-Z-_ .]{3,100}$')])),
                ('baja', models.BooleanField(default=False)),
                ('raza', models.CharField(error_messages={'blank': 'La especie es obligatorio', 'max_length': 'La especie puede tener a lo sumo 50 caracteres'}, help_text='Especie de la Mascota', max_length=50, validators=[django.core.validators.RegexValidator(regex='^[0-9a-zA-Z-_ .]{3,100}$')])),
                ('cliente', models.ForeignKey(error_messages={}, on_delete=django.db.models.deletion.CASCADE, to='GestionDeClientes.Cliente')),
            ],
        ),
    ]
