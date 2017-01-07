# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-07 14:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_user_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dog',
            old_name='uodated_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='instance',
            old_name='original_features',
            new_name='raw_features',
        ),
        migrations.RenameField(
            model_name='locationimg',
            old_name='lost_and_found',
            new_name='lost_and_found_id',
        ),
        migrations.AddField(
            model_name='dog',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
