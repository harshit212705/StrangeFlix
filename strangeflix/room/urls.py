# importing django modules
from django.urls import path, re_path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views as room_views


urlpatterns = [
    path('', room_views.index, name='index'),
    path('join/<str:room_id>/',room_views.room, name='room'),
    path('add_new_room/', room_views.add_new_room, name = "add_new_room"),
    path('get_host_rooms/',room_views.get_host_rooms, name = "get_host_rooms"),
    path('host_room_details/<str:room_id>', room_views.room_details,name = 'room_details'),
    path('member_room_details/<str:room_id>', room_views.member_room_details,name = 'member_room_details'),
    path('get_room_members/', room_views.get_room_members,name = 'get_room_members'),
    path('send_room_request/',room_views.send_room_request,name = 'send_room_request'),
    path('get_my_rooms/',room_views.get_my_rooms,name = 'get_my_rooms'),
    path('accept_room/',room_views.accept_room,name = 'accept_room'),
    path('reject_room/',room_views.reject_room,name = 'reject_room')
]