# importing django modules
from django.urls import path, re_path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views as provider_views


# defining url routes and corresponding function to be called in views
urlpatterns = [
    url('dashboard/', provider_views.provider_dashboard, name = "provider_dashboard"),
    url('add_new_series/', provider_views.add_new_series, name = "add_new_series"),
    url('add_new_season/', provider_views.add_new_season, name = "add_new_season"),
    url('add_new_episode/', provider_views.add_new_episode, name = "add_new_episode"),
    url('previously_uploaded_episodes/', provider_views.previously_uploaded_episodes, name = "previously_uploaded_episodes"),
    url('previously_uploaded_series/', provider_views.previously_uploaded_series, name = "previously_uploaded_series"),
    url('previously_uploaded_seasons/', provider_views.previously_uploaded_seasons, name = "previously_uploaded_seasons"),
    url('add_new_movie/', provider_views.add_new_movie, name = "add_new_movie"),
    url('add_movie_video/', provider_views.add_movie_video, name = "add_movie_video"),
    url('previously_uploaded_movies/', provider_views.previously_uploaded_movies, name = "previously_uploaded_movies"),
    url('previously_uploaded_movie_content/', provider_views.previously_uploaded_movie_content, name = "previously_uploaded_movie_content"),
    url('add_new_series_content/', provider_views.add_new_series_content, name = "add_new_series_content"),
    url('add_movie_free_content/', provider_views.add_movie_free_content, name = "add_movie_free_content"),
]
