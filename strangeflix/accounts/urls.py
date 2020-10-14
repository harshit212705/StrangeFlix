# importing django modules
from django.urls import path, re_path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views as account_views

# defining url routes and corresponding function to be called in views
urlpatterns = [
    url('register', account_views.user_registration, name = "account_register"),
    url('logout/',auth_views.LogoutView.as_view(), name="account_logout"),
    url('login',account_views.custom_login, name="account_login"),
    url('social_redirect_url',account_views.social_redirect_url, name="social_redirect_url"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/$',account_views.activate,name='account_register_activate'),
]