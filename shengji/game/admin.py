from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Room, Player, Message


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number',)


@admin.register(Player)
class PlayerAdmin(UserAdmin):
    list_display = ('username', 'room', 'is_active')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('player', 'content', 'timestamp')


admin.site.unregister(Group)
