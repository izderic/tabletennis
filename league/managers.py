from django.db.models import Manager, Q


class LeagueManager(Manager):
    def get_queryset(self):
        return super(LeagueManager, self).get_queryset().prefetch_related('players')


class LeagueRoundManager(Manager):
    def get_queryset(self):
        return super(LeagueRoundManager, self).get_queryset().select_related('league').prefetch_related('matches__sets')


class MatchManager(Manager):
    def get_queryset(self):
        return super(MatchManager, self).get_queryset()\
            .select_related('league_round__league', 'home_player', 'away_player', 'winner')\
            .prefetch_related('sets', 'league_round__league__players')


class SetManager(Manager):
    def get_queryset(self):
        return super(SetManager, self).get_queryset().select_related('match__league_round__league', 'match__home_player', 'match__away_player')

    def get_sets(self, player, league):
        """
        Returns the queryset of all sets for finished matches for player in the league.
        """
        return self.model.objects.filter(
            match__league_round__league=league,
            match__winner__isnull=False
        ).filter(Q(match__home_player=player) | Q(match__away_player=player))

class RankingManager(Manager):
    def get_queryset(self):
        return super(RankingManager, self).get_queryset().select_related('player', 'league')
