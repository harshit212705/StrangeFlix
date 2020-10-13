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
]
