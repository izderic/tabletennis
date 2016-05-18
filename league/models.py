from __future__ import unicode_literals
import collections

from django.db import models, transaction


class Player(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class League(models.Model):
    name = models.CharField(max_length=255)
    num_of_sets = models.PositiveSmallIntegerField(default=2)
    points_per_set = models.PositiveSmallIntegerField(default=6)
    players = models.ManyToManyField(Player)

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

    def __unicode__(self):
        return 'Round %d' % self.number


class Match(models.Model):
    league_round = models.ForeignKey(LeagueRound, related_name='matches')
    home_player = models.ForeignKey(Player, related_name='home_player')
    away_player = models.ForeignKey(Player, related_name='away_player')
    winner = models.ForeignKey(Player, related_name='winner', null=True)

    def __unicode__(self):
        return '%s %s' % (self.home_player.name, self.away_player.name)


class Set(models.Model):
    match = models.ForeignKey(Match, related_name='sets')
    home_player_score = models.PositiveSmallIntegerField()
    away_player_score = models.PositiveSmallIntegerField()
    number = models.PositiveSmallIntegerField()
