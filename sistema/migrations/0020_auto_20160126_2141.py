# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-26 21:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0019_ordenes_de_servicio_fecha_mail_enviado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factura',
            name='contacto_a_facturar',
        ),
        migrations.AddField(
            model_name='ordenes_de_servicio',
            name='contacto_servicio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sistema.Contactos'),
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='observaciones',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='tipo_cambio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='ordenes_de_servicio',
            name='observaciones',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
