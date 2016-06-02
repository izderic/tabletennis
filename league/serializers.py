from django.db import transaction
from rest_framework import serializers
from .models import Player, League, Match, Set, LeagueRound, Ranking


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

    def validate(self, attrs):
        instance = self.instance
        if instance:
            leagues = [league.name for league in League.objects.filter(players=instance)]
            if attrs['name'] != instance.name and leagues:
                raise serializers.ValidationError('Cannot change player name because the player is member of the following leagues: %s.' % ', '.join(leagues))

        return attrs


class LeagueSerializer(serializers.ModelSerializer):

    players = PlayerSerializer(many=True)

    class Meta:
        model = League
        fields = '__all__'

    def create(self, validated_data):
        league = League(
            name=validated_data['name'],
            num_of_sets=validated_data['num_of_sets'],
            points_per_set=validated_data['points_per_set']
        )

        names = []
        for player in validated_data['players']:
            names.append(player['name'])

        # TODO: Remove filtering by name
        players = Player.objects.filter(name__in=names)
        league.save(players=players)

        league.players = list(players)

        return league

    def update(self, instance, validated_data):
        instance.name=validated_data['name']
        instance.num_of_sets=validated_data['num_of_sets']
        instance.points_per_set=validated_data['points_per_set']

        names = []
        for player in validated_data['players']:
            names.append(player['name'])

        instance.save()
        # TODO: Remove filtering by name
        instance.players = list(Player.objects.filter(name__in=names))

        return instance


class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
    sets = SetSerializer(many=True)
    home_player = serializers.StringRelatedField()
    away_player = serializers.StringRelatedField()

    class Meta:
        model = Match
        fields = '__all__'
        depth = 2

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.update_match(validated_data)
        instance.update_rankings()

        return instance


class RoundSerializer(serializers.ModelSerializer):
    matches = MatchSerializer(many=True)
    class Meta:
        model = LeagueRound
        fields = '__all__'


class RankingSerializer(serializers.ModelSerializer):
    player = serializers.StringRelatedField()
    class Meta:
        model = Ranking
        fields = '__all__'