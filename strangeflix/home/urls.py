# importing django modules
from django.urls import path, include
from . import views as home_views

# defining url routes and corresponding function to be called in views
urlpatterns = [
    path('', home_views.HomeView.as_view(), name='home_page'),
]