from django.urls import path, re_path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views as admin_views

urlpatterns = [
    url('dashboard/', admin_views.admin_dashboard, name = "admin_dashboard"),
    url('get_series/',admin_views.get_series,name="get_series"),
    url('pending_uploaded_seasons/',admin_views.pending_uploaded_seasons,name="pending_uploaded_seasons"),
    url('pending_uploaded_episodes/',admin_views.pending_uploaded_episodes,name="pending_uploaded_episodes"),
    url('verify_video/',admin_views.verify_video,name="verify_video"),
    url('reject_video/',admin_views.reject_video,name="reject_video"),
    url('added_series/', admin_views.added_series, name = "added_series"),
    url('added_seasons/', admin_views.added_seasons, name = "added_seasons"),
    url('added_episodes/', admin_views.added_episodes, name = "added_episodes"),
    url('get_movies/',admin_views.get_movies,name="get_movies"),
    url('pending_movie_videos/',admin_views.pending_movie_videos,name="pending_movie_videos"),
    url('added_movies/', admin_views.added_movies, name = "added_movies"),
    url('added_movie_videos/', admin_views.added_movie_videos, name = "added_movie_videos"),
    url('search_users/', admin_views.search_users, name = "search_users"),
    url('change_user_type/', admin_views.change_user_type, name = "change_user_type"),
    url('update_user_type/', admin_views.update_user_type, name = "update_user_type"),
]