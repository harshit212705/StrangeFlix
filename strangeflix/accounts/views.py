from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import CustomUser as User
from .models import UserDetails
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import logout, login, views
from django.contrib.auth import authenticate
from subscribe.models import SubscriptionPlan
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm


#  imports required for Email Verification:-
from django.core.mail import EmailMessage, BadHeaderError
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode



def send_email(subject, html_message, to_email):
    """
    A Utility function to send Email
    :param subject: Subject of Email
    :param html_message: Message(Body) of Email (HTML Enabled)
    :param to_email: A list of Receivers' Email
    :return:True if email is sent successfully
    """
    from_email = settings.EMAIL_HOST_USER
    msg = EmailMessage(subject, html_message, from_email, to_email)
    msg.content_subtype = "html"
    try:
        msg.send()
        return True
    except BadHeaderError:
        return False



# For Registration/Signup of Users
def user_registration(request):
    if not request.user.is_authenticated:
        if request.method == "GET":
            # registration_form = CustomUserCreationForm()
            # login_form = AuthenticationForm()
            # context = {
            #     'registration_form': registration_form,
            #     'login_form': login_form,
            # }

            # return render(request, 'home/templates/home/index.html', context)
            raise Http404('Page not Found!!')

        elif request.method == 'POST':
            registration_form = CustomUserCreationForm(request.POST)
            if registration_form.is_valid():
                password1 = registration_form.cleaned_data['password1']
                password2 = registration_form.cleaned_data['password2']
                if password1 != password2:
                    return HttpResponse("Password Mismatch.")
                username = registration_form.cleaned_data['username']
                email = registration_form.cleaned_data['email']
                reg_user = User.objects.filter(email=email).first()
                if reg_user:
                    return HttpResponse("Email already registered. Try logging in!!")
                else:
                    reg_user = User.objects.filter(username=username).first()
                    if reg_user:
                        return HttpResponse("Username already registered. Try another one!!")
                    else:
                        user = registration_form.save(commit=False)
                        user.is_active = False
                        user.user_type = 'U'
                        user.save()
                        details = UserDetails.objects.create(user=user, wallet_money=0)
                        details.save()

                    # Sending email process starts
                    current_site = get_current_site(request)
                    mail_subject = 'Activate your StrangeFlix account.'
                    email_context = {
                        'user': user.username,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    }
                    html_message = render_to_string("accounts/acc_activate_email_template.html",
                                                    context=email_context)
                    to_email_list = [email]
                    if send_email(subject=mail_subject,
                                  html_message=html_message,
                                  to_email=to_email_list):  # to_email must be a tuple of list

                        response = f'A Confirmation email has been sent to {email}.' \
                                   f' Please visit the confirmation link to complete the registration and activate your account.'
                    else:
                        response = 'Mail can\'t be send now. Possible Cause - Connection Issue. Try again later sometime.'
                    return HttpResponse(response)
            else:
                print(registration_form.errors.as_data())
                for e in registration_form.errors:
                    for err in registration_form.errors[e].as_data():
                        return HttpResponse(err)
                return HttpResponse("Form InValid")
    else:
        return HttpResponse("A user is already Logged In.")



def activate(request, uidb64, token):
    """
        This function is called when user clicks the activation link sent to his account.
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token) and user.is_active == False:
        user.is_active = True
        user.save()
        login(request, user)
        if user.is_authenticated:
            # Asking user for subscribing to some plan
            subscription_plans = SubscriptionPlan.objects.all()
            context = {}
            count = 1
            for obj in subscription_plans:
                context.update({'plan_' + str(count): (obj.plan_duration, obj.plan_cost)})
                count += 1

            return render(request, 'subscribe/templates/subscribe/subscribe.html', {'context': context})

            return redirect("home_page") # Need to be changed
        else:
            return HttpResponse("Some Error Occured During Login.User Profile was not Created")
    else:
        return HttpResponse("ACTIVATION LINK IS INVALID")
