from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from .models import Player


class HomeView(TemplateView):
    template_name = 'league/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
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