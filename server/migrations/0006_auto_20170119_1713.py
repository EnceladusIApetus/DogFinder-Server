# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-19 10:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0005_auto_20170119_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
