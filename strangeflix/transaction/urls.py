from django.urls import path, re_path
from django.conf.urls import url
from . import views as transaction_views


urlpatterns = [
    url('wallet/', transaction_views.wallet_details, name='wallet_details'),
    url('add_money/', transaction_views.add_money, name='add_money'),
    url('add_money_details/', transaction_views.add_money_details, name='add_money_details'),
]
