"""
Defines urls for current app
"""
from django.conf.urls import url

from .views import PlayerListView, PlayerCreateView, PlayerUpdateView, PlayerDeleteView

urlpatterns = [
    url(r'^players/', PlayerListView.as_view(), name='league_players'),
    url(r'^player/create/', PlayerCreateView.as_view(), name='league_player_create'),
    url(r'^player/update/(?P<pk>\d+)/$', PlayerUpdateView.as_view(), name='league_player_update'),
    url(r'^player/delete/(?P<pk>\d+)/$', PlayerDeleteView.as_view(), name='league_player_delete')
]
