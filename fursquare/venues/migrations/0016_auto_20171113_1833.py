# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-13 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0015_auto_20171113_1534'),
    ]

    operations = [
        migrations.RenameField(
            model_name='venue',
            old_name='venue_address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='venue',
            old_name='venue_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='venue',
            old_name='venue_type',
            new_name='type',
        ),
        migrations.AddField(
            model_name='venue',
            name='description',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]