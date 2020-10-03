from django.db import models
from accounts.models import CustomUser as User
from subscribe.models import SubscriptionPlan


class TransactionDetails(models.Model):

    PAYMENT_TYPES = (

        # TYPES OF PAYMENTS
        ('C', 'Card'),
        ('W', 'Wallet'),
    )

    PAYMENT_STATUS_TYPES = (

        # TYPES OF PAYMENTS
        (1, 'Credit'),
        (2, 'Failed'),
        (3, 'Pending'),
        (4, 'Sent'),
        (5, 'Completed'),
    )

    transaction_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(User, on_delete=models.PROTECT)

    sub_plan_id = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)

    transaction_time = models.DateTimeField()

    payment_type = models.CharField(max_length=1, choices=PAYMENT_TYPES)

    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.PositiveSmallIntegerField(choices=PAYMENT_STATUS_TYPES)

    class Meta:
        verbose_name_plural = "Transaction Details"



# class TransactionToken(models.Model):

#     transaction_id = models.ForeignKey(TransactionDetails, on_delete=models.PROTECT)

#     token = 

#     class Meta:
#         verbose_name_plural = 'Transaction Tokens'
