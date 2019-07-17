from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^lobby/$', views.view_lobby, name='lobby'),
    url(r'^room/(?P<room_number>[1-9][0-9]{3})/$', views.view_room, name='room'),
    url(r'^create/room/$', views.create_room, name='create_room'),
    url(r'^join/room/$', views.join_room, name='_join_room'),
    url(r'^join/room/(?P<room_number>[1-9][0-9]{3})/$', views.join_room, name='join_room'),
]
