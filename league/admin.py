from django.contrib import admin
from .models import Player, League, LeagueRound, Match, Set


class SetInline(admin.StackedInline):
    model = Set


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    pass


@admin.register(LeagueRound)
class LeagueRoundAdmin(admin.ModelAdmin):
    pass


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('league_round', 'home_player', 'away_player', 'winner',)
    list_filter = ('league_round', 'winner',)
    inlines = [
        SetInline,
    ]

@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ('match', 'home_player_score', 'away_player_score',)
    list_filter = ('match',)
    list_per_page = 5
    search_fields = ['match__league_round__league__name']
