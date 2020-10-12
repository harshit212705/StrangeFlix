# importing django modules
from django.contrib import admin
from .models import TransactionDetails, TransactionToken, AddMoneyTransactionDetails


# registering models to admin panel
admin.site.register(TransactionDetails)
admin.site.register(TransactionToken)
admin.site.register(AddMoneyTransactionDetails)