from django.contrib import admin
from .models import TransactionDetails, TransactionToken, AddMoneyTransactionDetails

# Register your models here.
admin.site.register(TransactionDetails)
admin.site.register(TransactionToken)
admin.site.register(AddMoneyTransactionDetails)