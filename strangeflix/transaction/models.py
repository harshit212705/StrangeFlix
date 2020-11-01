# importing django modules
from django.db import models
from accounts.models import CustomUser as User
from subscribe.models import SubscriptionPlan

# model for storing transaction details
class TransactionDetails(models.Model):

    PAYMENT_TYPES = (

        # TYPES OF PAYMENTS
        ('C', 'Card'),
        ('W', 'Wallet'),
    )

    PAYMENT_REQUEST_STATUS_TYPES = (

        # TYPES OF PAYMENT REQUEST STATUS
        (1, 'Failed'),
        (2, 'Pending'),
        (3, 'Sent'),
        (4, 'Completed'),
        (5, 'Credit')
    )

    transaction_id = models.CharField(max_length=100,blank=True,default='', primary_key=True)

    user = models.ForeignKey(User, on_delete=models.PROTECT)

    sub_plan_id = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)

    transaction_start_time = models.DateTimeField()

    payment_type = models.CharField(max_length=1, choices=PAYMENT_TYPES)

    transaction_amount = models.IntegerField(default=0)

    status = models.PositiveSmallIntegerField(choices=PAYMENT_REQUEST_STATUS_TYPES)

    class Meta:
        verbose_name_plural = "Transaction Details"

    def __str__(self):
        return str('user--') + str(self.user.username) + str(' || plan_duration--') + str(self.sub_plan_id.plan_duration) + str(' || payment_type--') + str(self.payment_type) + str(' || transaction_amount--') + str(self.transaction_amount) + str(' || status--') + str(self.status) + str(' || transaction_id--') + str(self.transaction_id)



# model for storing transaction token details
class TransactionToken(models.Model):

    PAYMENT_STATUS_TYPES = (

        # TYPES OF PAYMENT STATUS
        (1, 'Failed'),
        (2, 'Credit'),
        (3, 'Refunded'),
    )

    transaction_id = models.ForeignKey(TransactionDetails, on_delete=models.PROTECT)

    payment_id = models.CharField(max_length=100,blank=True,default='')

    transaction_end_time = models.DateTimeField()

    status = models.PositiveSmallIntegerField(choices=PAYMENT_STATUS_TYPES, default=1)

    class Meta:
        verbose_name_plural = 'Transaction Tokens'

    def __str__(self):
        return str('transaction_id--') + str(self.transaction_id.transaction_id) + str(' || status--') + str(self.status)


# model for storing transaction details made for adding money to wallet
class AddMoneyTransactionDetails(models.Model):

    PAYMENT_STATUS_TYPES = (

        # TYPES OF PAYMENT STATUS
        (1, 'Failed'),
        (2, 'Pending'),
        (3, 'Sent'),
        (4, 'Completed'),
        (5, 'Credit'),
        (6, 'Refunded')
    )

    transaction_id = models.CharField(max_length=100,blank=True,default='', primary_key=True)

    user = models.ForeignKey(User, on_delete=models.PROTECT)

    transaction_start_time = models.DateTimeField()

    transaction_amount = models.IntegerField(default=0)

    status = models.PositiveSmallIntegerField(choices=PAYMENT_STATUS_TYPES)

    payment_id = models.CharField(max_length=100,blank=True,default='')

    class Meta:
        verbose_name_plural = "Add Money Transaction Details"

    def __str__(self):
        return str('user--') + str(self.user.username) + str(' || transaction_amount--') + str(self.transaction_amount) + str(' || status--') + str(self.status) + str(' || transaction_id--') + str(self.transaction_id)
