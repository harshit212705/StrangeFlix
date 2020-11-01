# importing django modules
from django.urls import path, re_path
from django.conf.urls import url
from . import views as transaction_views


# defining url routes and corresponding function to be called in views
urlpatterns = [
    url('wallet/', transaction_views.wallet_details, name='wallet_details'),
    url('add_money/', transaction_views.add_money, name='add_money'),
    url('add_money_details/', transaction_views.add_money_details, name='add_money_details'),
    url('check_payment_status/', transaction_views.check_payment_status, name='check_payment_status'),
]