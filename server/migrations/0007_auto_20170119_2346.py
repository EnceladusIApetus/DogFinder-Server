# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-19 16:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0006_auto_20170119_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
