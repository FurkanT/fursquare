# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 09:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0008_auto_20171108_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='total_vote_count',
            field=models.IntegerField(default=1),
        ),
    ]
