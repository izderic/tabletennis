from django.db import transaction
from rest_framework import serializers
from .models import Player, League, Match, Set, LeagueRound, Ranking


class PlayerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False)

    class Meta:
        model = Player
        fields = ('id', 'name',)

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

    def validate(self, attrs):
        instance = self.instance

        if len(attrs['players']) < 2:
            raise serializers.ValidationError('At least two players are required.')

        self._validate_if_changed(instance, attrs)
        return attrs

    def create(self, validated_data):
        instance = League()
        self._save_instance(instance, validated_data)
        return instance

    def update(self, instance, validated_data):
        self._save_instance(instance, validated_data)
        return instance

    def _save_instance(self, instance, validated_data):
        instance.name=validated_data['name']
        instance.num_of_sets=validated_data['num_of_sets']
        instance.points_per_set=validated_data['points_per_set']
        players = Player.objects.filter(pk__in=[player['id'] for player in validated_data['players']])
        instance.save(players=players)
        instance.players.set(list(players))

    def _validate_if_changed(self, instance, attrs):
        if instance and instance.has_started:
            error = False
            if attrs['name'] != instance.name:
                error = True
            elif attrs['num_of_sets'] != instance.num_of_sets:
                error = True
            elif attrs['points_per_set'] != instance.points_per_set:
                error = True
            else:
                existing = instance.players.all().values_list('id', flat=True)
                new = [item['id'] for item in attrs['players']]
                if set(new) != set(existing):
                    error = True
            if error:
                raise serializers.ValidationError('The league cannot be changed after it starts.')


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
