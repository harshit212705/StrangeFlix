from django.urls import path, re_path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views as admin_views

urlpatterns = [
    url('dashboard/', admin_views.admin_dashboard, name = "admin_dashboard"),
    url('get_series/',admin_views.get_series,name="get_series"),
]
