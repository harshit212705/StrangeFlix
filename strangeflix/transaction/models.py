from django.db import models
from accounts.models import CustomUser as User
from subscribe.models import SubscriptionPlan


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


class AddMoneyTransactionDetails(models.Model):

    PAYMENT_STATUS_TYPES = (

        # TYPES OF PAYMENT STATUS
        (1, 'Failed'),
        (2, 'Pending'),
        (3, 'Sent'),
        (4, 'Completed'),
        (5, 'Credit')
    )

    transaction_id = models.CharField(max_length=100,blank=True,default='', primary_key=True)

    user = models.ForeignKey(User, on_delete=models.PROTECT)

    transaction_start_time = models.DateTimeField()

    transaction_amount = models.IntegerField(default=0)

    status = models.PositiveSmallIntegerField(choices=PAYMENT_STATUS_TYPES)

    payment_id = models.CharField(max_length=100,blank=True,default='')

    class Meta:
        verbose_name_plural = "Add Money Transaction Details"
