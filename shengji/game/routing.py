from channels.routing import route

from . import consumers


channel_routing = [
    route('websocket.connect', consumers.chat_connect, path=r'^/chat/room/(?P<room_number>[1-9][0-9]{3})/$'),
    route('websocket.receive', consumers.chat_message, path=r'^/chat/room/(?P<room_number>[1-9][0-9]{3})/$'),
    route('websocket.disconnect', consumers.chat_disconnect, path=r'^/chat/room/(?P<room_number>[1-9][0-9]{3})/$'),

    route('websocket.connect', consumers.game_connect, path=r'^/game/room/(?P<room_number>[1-9][0-9]{3})/$'),
    route('websocket.receive', consumers.game_message, path=r'^/game/room/(?P<room_number>[1-9][0-9]{3})/$'),
    route('websocket.disconnect', consumers.game_disconnect, path=r'^/game/room/(?P<room_number>[1-9][0-9]{3})/$'),
]
