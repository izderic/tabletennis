# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-19 09:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'verbose_name_plural': 'matches'},
        ),
        migrations.AddField(
            model_name='set',
            name='finished',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='league',
            name='players',
            field=models.ManyToManyField(related_name='leagues', to='league.Player'),
        ),
    ]
