# importing django modules
from django.urls import path, include
from . import views as dashboard_views
from django.conf.urls import url

# defining url routes and corresponding function to be called in views
urlpatterns = [
    url('',dashboard_views.user_dashboard, name = "user_dashboard"),

]
