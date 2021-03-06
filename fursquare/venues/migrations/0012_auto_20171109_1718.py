# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 14:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0011_rating_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='venues.Venue'),
        ),
    ]
