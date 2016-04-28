from __future__ import unicode_literals

from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=30)


class League(models.Model):
    name = models.CharField(max_length=255)
    players = models.ManyToManyField(Player)


class LeagueRound(models.Model):
    league = models.ForeignKey(League)
    number = models.PositiveSmallIntegerField()


class Match(models.Model):
    league_round = models.ForeignKey(LeagueRound)
    home_player = models.ForeignKey(Player, related_name='home_player')
    away_player = models.ForeignKey(Player, related_name='away_player')
    winner = models.ForeignKey(Player, related_name='winner', null=True)


class Set(models.Model):
    match = models.ForeignKey(Match)
    home_player_score = models.PositiveSmallIntegerField()
    away_player_score = models.PositiveSmallIntegerField()
    number = models.PositiveSmallIntegerField()
