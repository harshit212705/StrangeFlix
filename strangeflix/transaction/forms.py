# importing django modules
from django import forms

# form for adding money to user wallet
class AddMoneyForm(forms.Form):
    amount = forms.IntegerField(required=True, max_value=100000, min_value=1)