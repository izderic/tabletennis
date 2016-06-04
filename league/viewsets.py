from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .models import Player, League, LeagueRound, Match, Set, Ranking
from .serializers import PlayerSerializer, LeagueSerializer, MatchSerializer, SetSerializer, RoundSerializer, RankingSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(data=data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        data = request.data
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.validate_players(data)
        serializer.save(data=data)
        return Response(serializer.data)


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
        rankings = rankings.order_by('-matches_won', '-set_difference', '-point_difference')
        return rankings
