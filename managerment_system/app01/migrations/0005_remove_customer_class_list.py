# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-06-17 08:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_auto_20190617_1502'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='class_list',
        ),
    ]
