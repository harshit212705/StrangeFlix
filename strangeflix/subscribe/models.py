# importing django models
from django.db import models
from accounts.models import CustomUser as User

# model for storing available subscription plans
class SubscriptionPlan(models.Model):

    sub_plan_id = models.AutoField(primary_key=True)

    plan_duration = models.IntegerField(blank=False, null=False)

    plan_cost = models.IntegerField(blank=False, null=False)

    class Meta:
        verbose_name_plural = "Subscription Plan"

    def __str__(self):
        return str('plan_id--') + str(self.sub_plan_id) + str(' || plan_duration--') + str(self.plan_duration) + str(' || plan_cost--') + str(self.plan_cost)


# importing transactionDetails model from transaction/models
from transaction.models import TransactionDetails as Transaction

# modlel for storing information about the subscription plans taken by the users
class Subscriptions(models.Model):

    subscription_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(User, on_delete=models.PROTECT)

    sub_plan_id = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)

    end_date = models.DateTimeField()

    transaction_id = models.ForeignKey(Transaction, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return str('user--') + str(self.user.username) + str(' || sub_plan--') + str(self.sub_plan_id.plan_duration) + str(' || end_date--') + str(self.end_date) + str(' || transaction_id--') + str(self.transaction_id.transaction_id)


# model for storing the transaction id in case the subscription amount is paid by both card and wallet
# so it generates to transaction ids
# one is stored in subscription model and additional one is stored in this model
class SubscriptionAdditionalTransaction(models.Model):

    subscription_id = models.ForeignKey(Subscriptions, on_delete=models.PROTECT)

    transaction_id = models.ForeignKey(Transaction, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Subscription Additional Transaction"

    def __str__(self):
        return str('subscription_id--') + str(self.subscription_id.subscription_id) + str(' || transaction_id--') + str(self.transaction_id.transaction_id)
