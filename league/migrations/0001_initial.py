# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-11 15:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='LeagueRound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField()),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.League')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_player_score', models.PositiveSmallIntegerField()),
                ('away_player_score', models.PositiveSmallIntegerField()),
                ('number', models.PositiveSmallIntegerField()),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.Match')),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='away_player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_player', to='league.Player'),
        ),
        migrations.AddField(
            model_name='match',
            name='home_player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_player', to='league.Player'),
        ),
        migrations.AddField(
            model_name='match',
            name='league_round',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.LeagueRound'),
        ),
        migrations.AddField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to='league.Player'),
        ),
        migrations.AddField(
            model_name='league',
            name='players',
            field=models.ManyToManyField(to='league.Player'),
        ),
    ]