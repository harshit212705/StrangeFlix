from django.shortcuts import render
from django.views.generic import View
from accounts.forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from subscribe.models import Subscriptions
from datetime import datetime
from django.utils import timezone

# function to render the mainpage or homepage
class HomeView(View):
    def get(self, request):
        registration_form = CustomUserCreationForm()
        login_form = AuthenticationForm()
        is_subscribed = False
        if request.user.is_authenticated:
            subscribe = Subscriptions.objects.filter(user=request.user, end_date__gt=datetime.now(tz=timezone.utc)).order_by('-end_date').first()
            if subscribe:
                is_subscribed = True

        context = {
            'registration_form': registration_form,
            'login_form': login_form,
            'is_subscribed': is_subscribed
        }
        return render(request, 'home/index.html', context)