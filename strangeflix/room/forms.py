from django import forms
from django.contrib.auth.models import User
from .models import RoomControl


class RoomCreationForm(forms.ModelForm):

	class Meta:
		model = RoomControl
		fields = ['title']