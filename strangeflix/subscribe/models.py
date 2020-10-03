from django.db import models
from accounts.models import CustomUser as User


class SubscriptionPlan(models.Model):

    sub_plan_id = models.AutoField(primary_key=True)

    plan_duration = models.IntegerField(blank=False, null=False)

    plan_cost = models.IntegerField(blank=False, null=False)

    class Meta:
        verbose_name_plural = "Subscription Plan"



from transaction.models import TransactionDetails as Transaction

class Subscriptions(models.Model):

    subscription_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(User, on_delete=models.PROTECT)

    sub_plan_id = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)

    end_date = models.DateTimeField()

    transaction_id = models.ForeignKey(Transaction, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Subscriptions"
