# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-06 12:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('venues', '0003_remove_venue_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='commented_to',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='venues.Venue'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venue',
            name='created_by',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venue',
            name='total_vote_counts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='venuetype',
            name='created_by',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
