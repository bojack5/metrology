# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-22 15:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0015_ordenes_de_servicio_mail_enviado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordenes_de_servicio',
            name='mail_enviado',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
    ]
