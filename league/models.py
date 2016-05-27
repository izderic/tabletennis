from __future__ import unicode_literals
import collections

from django.db import models, transaction
from django.db.models import Count
from .managers import LeagueManager, LeagueRoundManager, MatchManager, SetManager


class Player(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class League(models.Model):
    name = models.CharField(max_length=255)
    num_of_sets = models.PositiveSmallIntegerField(default=2)
    points_per_set = models.PositiveSmallIntegerField(default=6)
    players = models.ManyToManyField(Player, related_name='leagues')
    objects = LeagueManager()

    def __unicode__(self):
        return self.name

    @transaction.atomic
    def save(self, **kwargs):
        players = kwargs.pop('players', None)
        create = not self.pk
        super(League, self).save(**kwargs)

        if create and players:
            rounds = self._build_rounds(list(players.values_list('pk', flat=True)))

            for index, league_round in enumerate(rounds, start=1):
                league_round_obj = LeagueRound(league=self, number=index)
                league_round_obj.save()
                for match in league_round:

                    if u'x' in match:
                        continue

                    match_obj = Match(
                        league_round=league_round_obj,
                        home_player_id=match[0],
                        away_player_id=match[1]
                    )
                    match_obj.save()

    def get_rankings(self):
        players = Player.objects.filter(leagues=self)
        rankings = []
        for player in players:
            ranking = RankingObject(
                player=player.name,
                matches_played=0,
                matches_won=0,
                matches_lost=0
            )
            rankings.append(ranking)

        return rankings


    def _build_matches(self, l):
        a = []
        for i in range(len(l) / 2):
            a.append((l[i], l[-(i + 1)]))
        return a

    def _build_rounds(self, l):
        rounds = []

        if len(l) % 2 == 1:
            l.append('x')

        for i in range(len(l) - 1):
            d = collections.deque(l[1:])
            d.rotate(1)

            l = [l[0]] + list(d)

            matches = self._build_matches(l)
            rounds.append(matches)
            print matches

        rounds_switched = []
        for r in rounds:
            switched = map(lambda t: (t[1], t[0]), r)
            rounds_switched.append(switched)
            print switched

        return rounds + rounds_switched


class LeagueRound(models.Model):
    league = models.ForeignKey(League)
    number = models.PositiveSmallIntegerField()
    objects = LeagueRoundManager()

    def __unicode__(self):
        return '%s - Round %d' % (self.league, self.number)


class Match(models.Model):
    league_round = models.ForeignKey(LeagueRound, related_name='matches')
    home_player = models.ForeignKey(Player, related_name='home_player')
    away_player = models.ForeignKey(Player, related_name='away_player')
    winner = models.ForeignKey(Player, related_name='winner', null=True)
    objects = MatchManager()

    class Meta:
        verbose_name_plural = "matches"

    def __unicode__(self):
        return '%s: %s - %s' % (self.league_round.league, self.home_player.name, self.away_player.name)

    def update_match(self, validated_data):
        self.sets.all().delete()

        home = 0
        away = 0
        num_of_sets = self.league_round.league.num_of_sets

        for item in validated_data['sets']:

            home_player_score = item['home_player_score']
            away_player_score = item['away_player_score']

            Set.objects.create(
                home_player_score=home_player_score,
                away_player_score=away_player_score,
                match=self
            )
            if home_player_score > away_player_score:
                home += 1
            else:
                away += 1

        if home > away and home == num_of_sets:
            self.winner = self.home_player
        elif home < away and away == num_of_sets:
            self.winner = self.away_player
        else:
            self.winner = None

        self.save()

        return self


class Set(models.Model):
    match = models.ForeignKey(Match, related_name='sets')
    home_player_score = models.PositiveSmallIntegerField()
    away_player_score = models.PositiveSmallIntegerField()
    objects = SetManager()

    def __unicode__(self):
        return '%s: Set %d: %d - %d' % (self.match, self.number, self.home_player_score, self.away_player_score)


class RankingObject(object):
    def __init__(self, player, matches_played, matches_won, matches_lost):
        self.player = player
        self.matches_played = matches_played
        self.matches_won = matches_won
        self.matches_lost = matches_lost
