# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-15 13:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0018_auto_20171115_1313'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_date']},
        ),
        migrations.AlterField(
            model_name='venue',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='venues', to='venues.VenueType'),
        ),
    ]
