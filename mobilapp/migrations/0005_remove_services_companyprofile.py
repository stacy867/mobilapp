# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-12-03 12:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mobilapp', '0004_auto_20191203_1239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='services',
            name='companyprofile',
        ),
    ]
