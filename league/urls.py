"""
Defines urls for current app
"""
from django.conf.urls import url

from .views import PlayerListView, PlayerCreateView, PlayerUpdateView, PlayerDeleteView, LeagueListView, LeagueCreateView, LeagueUpdateView, LeagueDeleteView

urlpatterns = [
    # Player urls
    url(r'^players/', PlayerListView.as_view(), name='league_players'),
    url(r'^player/create/', PlayerCreateView.as_view(), name='league_player_create'),
    url(r'^player/update/(?P<pk>\d+)/$', PlayerUpdateView.as_view(), name='league_player_update'),
    url(r'^player/delete/(?P<pk>\d+)/$', PlayerDeleteView.as_view(), name='league_player_delete'),
    # League urls
    url(r'^leagues/', LeagueListView.as_view(), name='league_leagues'),
    url(r'^league/create/', LeagueCreateView.as_view(), name='league_league_create'),
    url(r'^league/update/(?P<pk>\d+)/$', LeagueUpdateView.as_view(), name='league_league_update'),
    url(r'^league/delete/(?P<pk>\d+)/$', LeagueDeleteView.as_view(), name='league_league_delete')
]
