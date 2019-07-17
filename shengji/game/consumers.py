import json

from channels import Group
from channels.sessions import enforce_ordering
from channels.auth import channel_session_user, channel_session_user_from_http

from .models import Room


@enforce_ordering
@channel_session_user_from_http
def chat_connect(message, room_number):
    message.reply_channel.send({
        'accept': True,
    })
    Group('chat-{}'.format(room_number)).add(message.reply_channel)


@enforce_ordering
@channel_session_user
def chat_message(message, room_number):
    payload = json.loads(message['text'])
    room = Room.objects.get(room_number=room_number)
    new_message = room.messages.create(player=message.user, content=payload['message'])
    new_payload = {
        'message': str(new_message),
    }
    Group('chat-{}'.format(room_number)).send({
        'text': json.dumps(new_payload),
    })


@enforce_ordering
@channel_session_user
def chat_disconnect(message, room_number):
    Group('chat-{}'.format(room_number)).discard(message.reply_channel)


@enforce_ordering
@channel_session_user_from_http
def game_connect(message, room_number):
    message.reply_channel.send({
        'accept': True,
    })
    Group('game-{}'.format(room_number)).add(message.reply_channel)
    new_payload = {
        'command': 'request_player_list',
    }
    Group('game-{}'.format(room_number)).send({
        'text': json.dumps(new_payload),
    })


@enforce_ordering
@channel_session_user
def game_message(message, room_number):
    payload = json.loads(message['text'])
    room = Room.objects.get(room_number=room_number)
    if payload['command'] == 'switch_player':
        room.switch_player(payload['from_player_order'], payload['to_player_order'])
        new_payload = {
            'command': 'request_player_list',
        }
        Group('game-{}'.format(room_number)).send({
            'text': json.dumps(new_payload),
        })
    elif payload['command'] == 'update_player_list':
        player_order_rotation_list = room.iterate_player(message.user)
        username_list = [room.get_username_by_player_order(player_order) for player_order in player_order_rotation_list]
        new_payload = {
            'command': 'new_player_list',
            'player_order_rotation_list': player_order_rotation_list,
            'username_list': username_list,
        }
        message.reply_channel.send({
            'text': json.dumps(new_payload),
        })


@enforce_ordering
@channel_session_user
def game_disconnect(message, room_number):
    Group('game-{}'.format(room_number)).discard(message.reply_channel)
