import itertools
import random

from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.utils import dateformat, timezone


class Room(models.Model):
    SIZE = 4
    PLAYER_ORDER_LIST = ('player_one_id', 'player_two_id', 'player_three_id', 'player_four_id')

    room_number = models.PositiveSmallIntegerField()
    player_one_id = models.IntegerField(blank=True, null=True)
    player_two_id = models.IntegerField(blank=True, null=True)
    player_three_id = models.IntegerField(blank=True, null=True)
    player_four_id = models.IntegerField(blank=True, null=True)

    @classmethod
    @transaction.atomic
    def create_room(cls):
        new_room = None
        while new_room is None:
            room_number = random.randrange(1000, 10000)
            if not cls.objects.filter(room_number=room_number).exists():
                new_room = cls.objects.create(room_number=room_number)
        return new_room

    @transaction.atomic
    def add_player(self, player):
        if self.players.count() < Room.SIZE and not self.players.filter(id=player.id).exists():
            self.players.add(player)
            for player_order in Room.PLAYER_ORDER_LIST:
                if getattr(self, player_order) is None:
                    setattr(self, player_order, player.id)
                    self.save()
                    break

    @transaction.atomic
    def switch_player(self, from_player_order, to_player_order):
        from_player_id = getattr(self, from_player_order)
        to_player_id = getattr(self, to_player_order)
        setattr(self, from_player_order, to_player_id)
        setattr(self, to_player_order, from_player_id)
        self.save()

    def iterate_player(self, player):
        player_order_rotation_list = list(itertools.islice(
            itertools.dropwhile(
                lambda x: getattr(self, x) != player.id,
                itertools.cycle(Room.PLAYER_ORDER_LIST)
            ),
            Room.SIZE
        ))
        return player_order_rotation_list

    def get_username_by_player_order(self, player_order):
        player_id = getattr(self, player_order)
        username = Player.objects.get(id=player_id).username if player_id is not None else ''
        return username

    def __str__(self):
        return '[{}]'.format(self.room_number)


class Player(AbstractUser):
    room = models.ForeignKey(Room, related_name='players', on_delete=models.SET_NULL, null=True)
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = 'player'

    def __str__(self):
        return '{} <{}>'.format(self.username, self.email)


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.SET_NULL, null=True)
    player = models.ForeignKey(Player, related_name='messages', null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    @property
    def time(self):
        return dateformat.time_format(timezone.localtime(self.timestamp), 'H:i:s')

    def __str__(self):
        if self.player is None:
            return '[{}] {}'.format(self.time, self.content)
        else:
            return '[{}] {}: {}'.format(self.time, self.player.username, self.content)


# class Game(models.Model):
#     SCORE_CHOICES = (
#         ('A', 'A'),
#         ('K', 'K'),
#         ('Q', 'Q'),
#         ('J', 'J'),
#         ('10', '10'),
#         ('9', '9'),
#         ('8', '8'),
#         ('7', '7'),
#         ('6', '6'),
#         ('5', '5'),
#         ('4', '4'),
#         ('3', '3'),
#         ('2', '2'),
#     )
#
#     room = models.OneToOneField(Room)
#     team_1_player_1 = models.OneToOneField(Player, null=True)
#     team_1_player_2 = models.OneToOneField(Player, null=True)
#     team_2_player_1 = models.OneToOneField(Player, null=True)
#     team_2_player_2 = models.OneToOneField(Player, null=True)
#     team_1_score = models.CharField(max_length=2, choices=SCORE_CHOICES, default='2')
#     team_2_score = models.CharField(max_length=2, choices=SCORE_CHOICES, default='2')
#     team_1_point = models.PositiveSmallIntegerField(default=0)
#     team_2_point = models.PositiveSmallIntegerField(default=0)
