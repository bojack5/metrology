# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-09 03:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0004_auto_20160109_0005'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cotizacion',
            old_name='kilometros',
            new_name='viajes',
        ),
        migrations.AddField(
            model_name='clientes',
            name='horas',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='tipo_cambio',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
