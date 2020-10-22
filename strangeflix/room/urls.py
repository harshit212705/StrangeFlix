# importing django modules
from django.urls import path, re_path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views as room_views


urlpatterns = [
    path('', room_views.index, name='index'),
    path('<str:room_name>/',room_views.room, name='room'),
]