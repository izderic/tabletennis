from __future__ import unicode_literals
import collections
import random

from django.db import models, transaction
from .managers import LeagueManager, LeagueRoundManager, MatchManager, SetManager, RankingManager


class Player(models.Model):
    """
    Simple player model.
    """
    name = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.name


class League(models.Model):
    """
    num_of_sets represents the number of sets needed to win the match.
    points_per_set represents the number of points needed to win the set.
    """
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
            rounds = League.build_rounds(list(players.values_list('pk', flat=True)))
            self._create_rounds(rounds)
            self._create_rankings(players)

    @property
    def has_started(self):
        """
        The league started if there are sets saved.
        """
        return Set.objects.filter(match__league_round__league=self).exists()

    def _create_rounds(self, rounds):
        """
        Saves LeagueRound objects based on generated rounds and create matches.
        """
        for index, league_round in enumerate(rounds, start=1):
            league_round_obj = LeagueRound(league=self, number=index)
            league_round_obj.save()
            League.create_matches(league_round, league_round_obj)

    def _create_rankings(self, players):
        """
        Creates new Ranking objects for specified players.
        """
        for player in players:
            Ranking.objects.create(
                league=self,
                player=player
            )

    @staticmethod
    def create_matches(league_round, league_round_obj):
        """
        Creates new Match objects based on generated round.
        """
        for match in league_round:
            if u'x' in match:
                continue

            Match.objects.create(
                league_round=league_round_obj,
                home_player_id=match[0],
                away_player_id=match[1]
            )

    @staticmethod
    def build_rounds(player_id_list):
        """
        Defines matches based on round-robin algorithm.
        https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm
        """
        rounds = []
        random.shuffle(player_id_list)

        if len(player_id_list) % 2 == 1:
            player_id_list.append('x')

        for i in range(len(player_id_list) - 1):
            player_deque = collections.deque(player_id_list[1:])
            player_deque.rotate(1)
            player_id_list = [player_id_list[0]] + list(player_deque)
            matches = League.build_matches(player_id_list)
            rounds.append(matches)

        rounds_switched = []
        for r in rounds:
            switched = map(lambda t: (t[1], t[0]), r)
            rounds_switched.append(switched)

        return rounds + rounds_switched

    @staticmethod
    def build_matches(player_id_list):
        """
        Defines matches in the round.
        """
        match_list = []
        for i in range(len(player_id_list) / 2):
            match_list.append((player_id_list[i], player_id_list[-(i + 1)]))
        return match_list


class LeagueRound(models.Model):
    """
    LeagueRound model. Round has the number within the league.
    """
    league = models.ForeignKey(League, related_name='rounds')
    number = models.PositiveSmallIntegerField()
    objects = LeagueRoundManager()

    def __unicode__(self):
        return '%s - Round %d' % (self.league, self.number)


class Match(models.Model):
    """
    Defines the match between two players.
    """
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
        """
        Creates sets and saves match winner.
        """
        self.sets.all().delete()

        home = 0
        away = 0
        num_of_sets = self.league_round.league.num_of_sets

        for item in validated_data['sets']:
            home_player_score = item['home_player_score']
            away_player_score = item['away_player_score']

            if home_player_score > away_player_score:
                set_winner = self.home_player
            else:
                set_winner = self.away_player

            Set.objects.create(
                home_player_score=home_player_score,
                away_player_score=away_player_score,
                match=self,
                winner=set_winner
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
        """
        Updates the league ranking of home and away player.
        """
        league = self.league_round.league
        Match.update_player_ranking(self.home_player, league)
        Match.update_player_ranking(self.away_player, league)

    @staticmethod
    def update_player_ranking(player, league):
        """
        Updates the current league ranking for single player.
        """
        ranking = Ranking.objects.get(player=player, league=league)
        home_matches_won, home_matches_lost, away_matches_won, away_matches_lost = Match.calculate_won_lost(player, league)

        home_matches_played = home_matches_won + home_matches_lost
        away_matches_played = away_matches_won + away_matches_lost

        ranking.matches_played = home_matches_played + away_matches_played
        ranking.matches_won = home_matches_won + away_matches_won
        ranking.matches_lost = home_matches_lost + away_matches_lost

        # Home
        ranking.home_matches_played = home_matches_played
        ranking.home_matches_won = home_matches_won
        ranking.home_matches_lost = home_matches_lost

        # Away
        ranking.away_matches_played = away_matches_played
        ranking.away_matches_won = away_matches_won
        ranking.away_matches_lost = away_matches_lost

        sets_won, sets_lost, points_won, points_lost = Match.calculate_sets_points(player, league)

        ranking.sets_won = sets_won
        ranking.sets_lost = sets_lost
        ranking.set_difference = sets_won - sets_lost
        ranking.points_won = points_won
        ranking.points_lost = points_lost
        ranking.point_difference = points_won - points_lost

        ranking.save()

    @staticmethod
    def calculate_won_lost(player, league):
        """
        Calculates and returns the number of matches won and lost, home and away.
        """
        home_matches = player.home_matches.filter(league_round__league=league, winner__isnull=False)
        away_matches = player.away_matches.filter(league_round__league=league, winner__isnull=False)
        home_matches_won, home_matches_lost = Match.count_won_lost(home_matches, player)
        away_matches_won, away_matches_lost = Match.count_won_lost(away_matches, player)

        return home_matches_won, home_matches_lost, away_matches_won, away_matches_lost

    @staticmethod
    def count_won_lost(matches, player):
        """
        Counts the number of won and lost matches.
        """
        matches_won = 0
        matches_lost = 0
        for match in matches:
            if match.winner == player:
                matches_won += 1
            else:
                matches_lost += 1
        return matches_won, matches_lost

    @staticmethod
    def calculate_sets_points(player, league):
        """
        Calculates the number of sets and points, won and lost.
        """
        sets_won = 0
        sets_lost = 0
        points_won = 0
        points_lost = 0

        sets = Set.objects.get_sets(player, league)

        for set_obj in sets:
            if player == set_obj.winner:
                sets_won += 1
            else:
                sets_lost += 1
            if player == set_obj.match.home_player:
                points_won += set_obj.home_player_score
                points_lost += set_obj.away_player_score
            else:
                points_won += set_obj.away_player_score
                points_lost += set_obj.home_player_score

        return sets_won, sets_lost, points_won, points_lost


class Set(models.Model):
    """
    Defines the model for set in the match.
    """
    match = models.ForeignKey(Match, related_name='sets')
    home_player_score = models.PositiveSmallIntegerField()
    away_player_score = models.PositiveSmallIntegerField()
    winner = models.ForeignKey(Player, related_name='winner_sets', null=True)
    objects = SetManager()

    def __unicode__(self):
        return '%s: Set %d - %d' % (self.match, self.home_player_score, self.away_player_score)


class Ranking(models.Model):
    """
    Player ranking in the league.
    """
    league = models.ForeignKey(League, related_name='rankings')
    player = models.ForeignKey(Player, related_name='rankings')

    # Total
    matches_played = models.PositiveSmallIntegerField(default=0)
    matches_won = models.PositiveSmallIntegerField(default=0)
    matches_lost = models.PositiveSmallIntegerField(default=0)
    sets_won = models.PositiveSmallIntegerField(default=0)
    sets_lost = models.PositiveSmallIntegerField(default=0)
    set_difference = models.IntegerField(default=0)
    points_won = models.PositiveSmallIntegerField(default=0)
    points_lost = models.PositiveSmallIntegerField(default=0)
    point_difference = models.IntegerField(default=0)

    # Home
    home_matches_played = models.PositiveSmallIntegerField(default=0)
    home_matches_won = models.PositiveSmallIntegerField(default=0)
    home_matches_lost = models.PositiveSmallIntegerField(default=0)

    # Away
    away_matches_played = models.PositiveSmallIntegerField(default=0)
    away_matches_won = models.PositiveSmallIntegerField(default=0)
    away_matches_lost = models.PositiveSmallIntegerField(default=0)

    objects = RankingManager()

    class Meta:
        unique_together = ('league', 'player')

    def __unicode__(self):
        return '%s - %s' % (self.league.name, self.player.name)
