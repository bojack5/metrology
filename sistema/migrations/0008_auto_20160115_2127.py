# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-15 21:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0007_auto_20160113_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotizacion',
            name='importe',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]