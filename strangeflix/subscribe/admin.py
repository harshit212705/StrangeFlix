# importing django modules
from django.contrib import admin
from .models import SubscriptionPlan, Subscriptions, SubscriptionAdditionalTransaction


# registering models to admin panel
admin.site.register(SubscriptionPlan)
admin.site.register(Subscriptions)
admin.site.register(SubscriptionAdditionalTransaction)
