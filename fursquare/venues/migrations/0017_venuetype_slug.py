# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-15 10:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0016_auto_20171113_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='venuetype',
            name='slug',
            field=models.SlugField(default='slug'),
        ),
    ]
