# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-06 11:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0002_auto_20171106_1429'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venue',
            name='comment',
        ),
    ]
