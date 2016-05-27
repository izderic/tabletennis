from rest_framework import viewsets

from .models import Player, League, LeagueRound, Match, Set, Ranking
from .serializers import PlayerSerializer, LeagueSerializer, MatchSerializer, SetSerializer, RoundSerializer, RankingSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer


class RoundViewSet(viewsets.ModelViewSet):
    queryset = LeagueRound.objects.all()
    serializer_class = RoundSerializer

    def get_queryset(self):
        rounds = super(RoundViewSet, self).get_queryset()
        league = self.request.query_params.get('league')
        if league:
            rounds = rounds.filter(league=league)
        return rounds


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class SetViewSet(viewsets.ModelViewSet):
    queryset = Set.objects.all()
    serializer_class = SetSerializer


class RankingViewSet(viewsets.ModelViewSet):
    queryset = Ranking.objects.all()
    serializer_class = RankingSerializer

    def get_queryset(self):
        rankings = super(RankingViewSet, self).get_queryset()
        league = self.request.query_params.get('league')
        if league:
            rankings = rankings.filter(league=league)
        rankings = rankings.order_by('-matches_won')
        return rankings
