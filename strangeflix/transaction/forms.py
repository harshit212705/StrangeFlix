from django import forms


class AddMoneyForm(forms.Form):
    amount = forms.IntegerField(required=True, max_value=100000, min_value=1)