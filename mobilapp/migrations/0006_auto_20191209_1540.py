# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-12-09 15:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mobilapp', '0005_auto_20191209_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='service',
            field=models.ForeignKey(blank=True,null=True, on_delete=django.db.models.deletion.CASCADE, to='mobilapp.Services'),
            preserve_default=False,
        ),
    ]