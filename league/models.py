from __future__ import unicode_literals
import collections
import random

from django.db import models, transaction
from .managers import LeagueManager, LeagueRoundManager, MatchManager, SetManager, RankingManager


class Player(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class League(models.Model):
    name = models.CharField(max_length=255, unique=True)
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

        if create or not self.has_started:
            self.rounds.all().delete()
            self.rankings.all().delete()
            rounds = self._build_rounds(list(players.values_list('pk', flat=True)))
            self._create_rounds(rounds)
            self._create_rankings(players)

    @property
    def has_started(self):
        """
        The league started if there are sets saved.
        """
        return Set.objects.filter(match__league_round__league=self).exists()

    def _create_rounds(self, rounds):
        for index, league_round in enumerate(rounds, start=1):
            league_round_obj = LeagueRound(league=self, number=index)
            league_round_obj.save()
            self._create_matches(league_round, league_round_obj)

    def _create_matches(self, league_round, league_round_obj):
        for match in league_round:
            if u'x' in match:
                continue

            match_obj = Match(
                league_round=league_round_obj,
                home_player_id=match[0],
                away_player_id=match[1]
            )
            match_obj.save()

    def _create_rankings(self, players):
        for player in players:
            Ranking.objects.create(
                league = self,
                player = player
            )

    def _build_matches(self, player_id_list):
        match_list = []
        for i in range(len(player_id_list) / 2):
            match_list.append((player_id_list[i], player_id_list[-(i + 1)]))
        return match_list

    def _build_rounds(self, player_id_list):
        rounds = []

        random.shuffle(player_id_list)

        if len(player_id_list) % 2 == 1:
            player_id_list.append('x')

        for i in range(len(player_id_list) - 1):
            player_deque = collections.deque(player_id_list[1:])
            player_deque.rotate(1)
            player_id_list = [player_id_list[0]] + list(player_deque)
            matches = self._build_matches(player_id_list)
            rounds.append(matches)

        rounds_switched = []
        for r in rounds:
            switched = map(lambda t: (t[1], t[0]), r)
            rounds_switched.append(switched)

        return rounds + rounds_switched


class LeagueRound(models.Model):
    league = models.ForeignKey(League, related_name='rounds')
    number = models.PositiveSmallIntegerField()
    objects = LeagueRoundManager()

    def __unicode__(self):
        return '%s - Round %d' % (self.league, self.number)


class Match(models.Model):
    league_round = models.ForeignKey(LeagueRound, related_name='matches')
    home_player = models.ForeignKey(Player, related_name='home_matches')
    away_player = models.ForeignKey(Player, related_name='away_matches')
    winner = models.ForeignKey(Player, related_name='winner_matches', null=True)
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

        if home == num_of_sets:
            self.winner = self.home_player
        elif away == num_of_sets:
            self.winner = self.away_player
        else:
            self.winner = None

        self.save()

        return self

    def update_rankings(self):
        home_player = self.home_player
        away_player = self.away_player
        league = self.league_round.league
        self._update_player_ranking(home_player, league)
        self._update_player_ranking(away_player, league)

    def _update_player_ranking(self, player, league):
        matches_won, matches_lost = self._calculate_won_lost(player, league)
        ranking = Ranking.objects.get(player=player, league=league)
        ranking.matches_won = matches_won
        ranking.matches_lost = matches_lost
        ranking.matches_played = matches_won + matches_lost
        ranking.save()

    def _calculate_won_lost(self, player, league):
        matches_won = 0
        matches_lost = 0
        home_matches = player.home_matches.filter(league_round__league=league)
        away_matches = player.away_matches.filter(league_round__league=league)
        player_matches = home_matches | away_matches

        for match in player_matches:
            if match.winner:
                if match.winner == player:
                    matches_won += 1
                else:
                    matches_lost += 1

        return matches_won, matches_lost


class Set(models.Model):
    match = models.ForeignKey(Match, related_name='sets')
    home_player_score = models.PositiveSmallIntegerField()
    away_player_score = models.PositiveSmallIntegerField()
    objects = SetManager()

    def __unicode__(self):
        return '%s: Set %d - %d' % (self.match, self.home_player_score, self.away_player_score)


class Ranking(models.Model):
    league = models.ForeignKey(League, related_name='rankings')
    player = models.ForeignKey(Player, related_name='rankings')
    matches_played = models.PositiveSmallIntegerField(default=0)
    matches_won = models.PositiveSmallIntegerField(default=0)
    matches_lost = models.PositiveSmallIntegerField(default=0)
    sets_won = models.PositiveSmallIntegerField(default=0)
    sets_lost = models.PositiveSmallIntegerField(default=0)
    objects = RankingManager()

    class Meta:
        unique_together = ('league', 'player')

    def __unicode__(self):
        return '%s - %s' % (self.league.name, self.player.name)
