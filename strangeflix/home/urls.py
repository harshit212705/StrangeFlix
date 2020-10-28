# importing django modules
from django.urls import path, include
from . import views as home_views
from django.conf.urls import url

# defining url routes and corresponding function to be called in views
urlpatterns = [
    url('get_movie_details/', home_views.get_movie_details, name = "get_movie_details"),
    url('get_series_details/', home_views.get_series_details, name = "get_series_details"),
    url('get_season_details/', home_views.get_season_details, name = "get_season_details"),
    url('check_user_subscription/', home_views.check_user_subscription, name = "check_user_subscription"),
    url('report_comment/', home_views.report_comment, name = "report_comment"),
    url('report_video/', home_views.report_video, name = "report_video"),
    url('add_to_favourite/', home_views.add_to_favourite, name = "add_to_favourite"),
    url('add_video_comment/', home_views.add_video_comment, name = "add_video_comment"),
    url('check_min_wallet_bal/', home_views.check_min_wallet_bal, name = "check_min_wallet_bal"),
    url('get_pay_per_view_video/', home_views.get_pay_per_view_video, name = "get_pay_per_view_video"),


    url('rate_movie/', home_views.rate_movie, name = "rate_movie"),
    url('rate_series/', home_views.rate_series, name = "rate_series"),
    url(r'^video/(?P<video_id>[0-9]+)/$', home_views.fetch_video, name = "fetch_video"),
    path('', home_views.HomeView.as_view(), name='home_page'),
]
