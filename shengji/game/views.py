from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Room, Message


def index(request):
    if request.user.is_authenticated:
        return redirect(view_lobby)
    else:
        return render(request, 'game/index.html')


@login_required
def view_lobby(request):
    return render(request, 'game/lobby.html')


@login_required
def view_room(request, room_number):
    room = Room.objects.get(room_number=room_number)
    if request.user.room == room:
        messages = room.messages.order_by('timestamp')
        player_order_rotation_list = room.iterate_player(request.user)
        username_list = [room.get_username_by_player_order(player_order) for player_order in player_order_rotation_list]
        return render(request, 'game/room.html', {
            'room': room,
            'messages': messages,
            'bottom_username': username_list[0],
            'right_username': username_list[1],
            'top_username': username_list[2],
            'left_username': username_list[3],
        })
    else:
        return redirect(view_lobby)


@login_required
def create_room(request):
    new_room = Room.create_room()
    return redirect(join_room, room_number=new_room.room_number)


@login_required
def join_room(request, room_number=None):
    if request.method == 'POST':
        room_number = request.POST.get('room-number')
    room = Room.objects.get(room_number=room_number)
    room.add_player(request.user)
    return redirect(view_room, room_number=room_number)
