# importing django modules
from django.urls import path, re_path
from django.conf.urls import url
from . import views as subscribe_views


# defining url routes and corresponding function to be called in views
urlpatterns = [
    url(r'^(?P<plan_id>[0-9]+)/$', subscribe_views.subscribe_plan, name='subscribe_plan'),
    url(r'^ajax/use_wallet_bal/$', subscribe_views.use_wallet_bal, name='use_wallet_bal'),
    url(r'^payment/(?P<plan_id>[0-9]+)/$',subscribe_views.make_payment,name='make_payment'),
    url(r'^payment_details/$', subscribe_views.payment_details, name='payment_details'),
    url(r'$', subscribe_views.subscription_plans, name='subscription_plans'),
]