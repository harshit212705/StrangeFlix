from django.contrib import admin
from .models import SubscriptionPlan, Subscriptions

# Register your models here.

admin.site.register(SubscriptionPlan)
admin.site.register(Subscriptions)
