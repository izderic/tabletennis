from django.db.models import Manager


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


class RankingManager(Manager):
    def get_queryset(self):
        return super(RankingManager, self).get_queryset().select_related('player', 'league')
