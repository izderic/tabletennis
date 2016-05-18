import json

from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse

from rest_framework import viewsets

from .models import Player, League, Match, Set, LeagueRound
from .forms import LeagueForm
from .serializers import PlayerSerializer, LeagueSerializer, MatchSerializer, SetSerializer, RoundSerializer


class HomeView(TemplateView):
    template_name = 'league/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['page_title'] = "Home"
        return context


class PlayerListView(ListView):
    model = Player

    def get_context_data(self, **kwargs):
        context = super(PlayerListView, self).get_context_data(**kwargs)
        context['page_title'] = "Players"
        return context


class PlayerCreateView(CreateView):
    model = Player
    fields = ['name']
    success_url = reverse_lazy('league_players')

    def get_context_data(self, **kwargs):
        context = super(PlayerCreateView, self).get_context_data(**kwargs)
        context['page_title'] = "Create Player"
        return context


class PlayerUpdateView(UpdateView):
    model = Player
    fields = ['name']
    success_url = reverse_lazy('league_players')

    def get_context_data(self, **kwargs):
        context = super(PlayerUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = "Edit Player"
        return context


class PlayerDeleteView(DeleteView):
    model = Player
    success_url = reverse_lazy('league_players')

    def get_context_data(self, **kwargs):
        context = super(PlayerDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = "Delete Player"
        return context


class LeagueListView(ListView):
    model = League

    def get_queryset(self):
        queryset = super(LeagueListView, self).get_queryset()
        return queryset.prefetch_related('players')

    def get_context_data(self, **kwargs):
        context = super(LeagueListView, self).get_context_data(**kwargs)
        context['page_title'] = "Leagues"
        return context


class LeagueCreateView(CreateView):
    model = League
    form_class = LeagueForm
    success_url = reverse_lazy('league_leagues')

    def get_context_data(self, **kwargs):
        context = super(LeagueCreateView, self).get_context_data(**kwargs)
        context['page_title'] = "Create League"
        return context

    def form_valid(self, form):
        form.save(players=form.cleaned_data.get('players'))
        return HttpResponseRedirect(reverse_lazy('league_leagues'))


class LeagueUpdateView(UpdateView):
    model = League
    form_class = LeagueForm
    success_url = reverse_lazy('league_leagues')

    def get_context_data(self, **kwargs):
        context = super(LeagueUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = "Edit League"
        return context


class LeagueDeleteView(DeleteView):
    model = League
    success_url = reverse_lazy('league_leagues')

    def get_context_data(self, **kwargs):
        context = super(LeagueDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = "Delete League"
        return context


class MatchesView(TemplateView):
    template_name = 'league/matches.html'

    def get_context_data(self, **kwargs):
        league_id = kwargs.pop('pk', None)
        context = super(MatchesView, self).get_context_data(**kwargs)
        context['page_title'] = "Matches"

        matches_queryset = Match.objects.filter(league_round__league=league_id).select_related()
        rounds = []

        rounds_dict = {}
        for match in matches_queryset:
            match_list = rounds_dict.get(match.league_round, [])
            match_list.append(match)
            rounds_dict[match.league_round] = match_list

            if match.league_round not in rounds:
                rounds.append(match.league_round)

        matches = []
        for item in rounds:
            matches.append(rounds_dict[item])

        context['rounds'] = zip(rounds, matches)
        return context


class MainView(TemplateView):
    template_name = 'main.html'


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer


class MatchViewSet(viewsets.ModelViewSet):

    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class SetViewSet(viewsets.ModelViewSet):
    queryset = Set.objects.all()
    serializer_class = SetSerializer


class RoundViewSet(viewsets.ModelViewSet):

    queryset = LeagueRound.objects.all()
    serializer_class = RoundSerializer

    # Optimize queries
    def get_queryset(self):
        rounds = LeagueRound.objects.all().prefetch_related('matches').prefetch_related('matches__sets')
        return rounds
