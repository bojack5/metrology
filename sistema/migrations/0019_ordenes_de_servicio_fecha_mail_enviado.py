# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-22 20:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0018_auto_20160122_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordenes_de_servicio',
            name='fecha_mail_enviado',
            field=models.DateField(blank=True, null=True),
        ),
    ]
