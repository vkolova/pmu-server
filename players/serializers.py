from django.contrib.auth.models import User
from rest_framework import serializers

# from games.serializers import Game
from .models import Player

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')


class SimplePlayerSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Player
        fields = ('id', 'avatar', 'username')
        read_only_fields = ('id', 'username')

    username = serializers.SerializerMethodField()
    avatar = serializers.URLField(max_length=5000, min_length=None, allow_blank=True)

    def get_username(self, obj):
        return obj.user.username


class PlayerSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Player
        fields = ('id', 'user', 'score', 'avatar', 'level', 'games', 'wins', 'streak', 'push_notification_token', 'rang_position')
        read_only_fields = ('level', 'games', 'wins', 'streak', 'rang_position',)
        write_once_fields = ('user',)
    
    user = UserSerializer()
    push_notification_token = serializers.CharField(max_length=50, allow_blank=True)
    score = serializers.IntegerField()
    avatar = serializers.URLField(max_length=5000, min_length=None, allow_blank=True)
    level = serializers.SerializerMethodField()
    games = serializers.SerializerMethodField()
    wins = serializers.SerializerMethodField()
    streak = serializers.SerializerMethodField()
    rang_position = serializers.SerializerMethodField()

    def get_level(self, obj):
        level = obj.score / 100
        return int(level) + 1
    
    def get_games(self, obj):
        return obj.games.filter(state='finished').count()

    def get_wins(self, obj):
        return obj.games.filter(winner__id=obj.id).count()

    def get_streak(self, obj):
        games = obj.games.filter(state='finished').order_by('-id')
        streak = 0
        for g in games:
            if g.winner:
                if g.winner.id is obj.id:
                    streak = streak + 1
                else:
                    return streak
        return streak
    
    def get_rang_position(self, obj):
        queryset = Player.objects.all().order_by('-score')
        return list(queryset.values_list('pk', flat=True)).index(obj.pk) + 1