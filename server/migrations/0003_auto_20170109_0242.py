# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-08 19:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_auto_20170109_0240'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='lost_and_found_id',
            new_name='lost_and_found',
        ),
        migrations.RenameField(
            model_name='locationimg',
            old_name='lost_and_found_id',
            new_name='lost_and_found',
        ),
    ]
