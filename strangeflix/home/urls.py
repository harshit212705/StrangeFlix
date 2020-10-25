# importing django modules
from django.urls import path, include
from . import views as home_views
from django.conf.urls import url

# defining url routes and corresponding function to be called in views
urlpatterns = [
    url('get_movie_details/', home_views.get_movie_details, name = "get_movie_details"),
    url('get_series_details/', home_views.get_series_details, name = "get_series_details"),
    url('get_season_details/', home_views.get_season_details, name = "get_season_details"),
    # url('stream_movie/', home_views.stream_movie, name = "stream_movie"),
    url('rate_movie/', home_views.rate_movie, name = "rate_movie"),
    url('rate_series/', home_views.rate_series, name = "rate_series"),
    url(r'^video/(?P<video_id>[0-9]+)/$', home_views.fetch_video, name = "fetch_video"),
    # url('stream_video/', home_views.stream_video, name = "stream_video"),
    path('', home_views.HomeView.as_view(), name='home_page'),
]
