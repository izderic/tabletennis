from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from .models import Player, League


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
    template_name = "league/confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super(PlayerDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = "Delete Player"
        return context


class LeagueListView(ListView):
    model = League

    def get_context_data(self, **kwargs):
        context = super(LeagueListView, self).get_context_data(**kwargs)
        context['page_title'] = "Leagues"
        return context


class LeagueCreateView(CreateView):
    model = League
    fields = ['name', 'num_of_sets', 'points_per_set', 'players']
    success_url = reverse_lazy('league_leagues')

    def get_context_data(self, **kwargs):
        context = super(LeagueCreateView, self).get_context_data(**kwargs)
        context['page_title'] = "Create League"
        return context


class LeagueUpdateView(UpdateView):
    model = League
    fields = ['name', 'num_of_sets', 'points_per_set', 'players']
    success_url = reverse_lazy('league_leagues')

    def get_context_data(self, **kwargs):
        context = super(LeagueUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = "Edit League"
        return context


class LeagueDeleteView(DeleteView):
    model = League
    success_url = reverse_lazy('league_leagues')
    template_name = "league/confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super(LeagueDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = "Delete League"
        return context