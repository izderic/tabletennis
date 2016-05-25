from rest_framework import serializers
from .models import Player, League, Match, Set, LeagueRound


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class LeagueSerializer(serializers.ModelSerializer):

    players = PlayerSerializer(many=True)

    class Meta:
        model = League
        fields = ('id', 'name', 'num_of_sets', 'points_per_set', 'players')

    def create(self, validated_data):
        league = League(
            name=validated_data['name'],
            num_of_sets=validated_data['num_of_sets'],
            points_per_set=validated_data['points_per_set']
        )

        names = []
        for player in validated_data['players']:
            names.append(player['name'])

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

    def update(self, instance, validated_data):

        instance.sets.all().delete()

        home = 0
        away = 0

        for item in validated_data['sets']:

            home_player_score = item['home_player_score']
            away_player_score = item['away_player_score']

            Set.objects.create(
                home_player_score=home_player_score,
                away_player_score=away_player_score,
                match=instance
            )
            if home_player_score > away_player_score:
                home += 1
            else:
                away += 1

        if home > away:
            instance.winner = instance.home_player
        elif home < away:
            instance.winner = instance.away_player

        instance.save()

        return instance


class RoundSerializer(serializers.ModelSerializer):
    matches = MatchSerializer(many=True)
    class Meta:
        model = LeagueRound
        fields = '__all__'
