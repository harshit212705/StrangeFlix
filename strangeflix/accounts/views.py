# django modules
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth import logout, login, views
from django.contrib.auth import authenticate
from subscribe.models import SubscriptionPlan
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
import json

# importing models
from .models import CustomUser as User
from .models import UserDetails

# importing forms
from .forms import CustomUserCreationForm, CustomUserChangeForm

#  imports required for Email Verification:-
from django.core.mail import EmailMessage, BadHeaderError
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


# function to send email to user
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
            return render(request, 'templates/404.html')

        elif request.method == 'POST':
            # extracting form data for user registration
            registration_form = CustomUserCreationForm(request.POST)

            # checking the validity of the form
            if registration_form.is_valid():
                password1 = registration_form.cleaned_data['password1']
                password2 = registration_form.cleaned_data['password2']

                # password and confirm password mismatch error
                if password1 != password2:
                    return HttpResponse("Password Mismatch.")
                username = registration_form.cleaned_data['username']
                email = registration_form.cleaned_data['email']
                reg_user = User.objects.filter(email=email).first()

                # checking if email is already registered
                if reg_user:
                    return HttpResponse("Email already registered. Try logging in!!")
                else:
                    reg_user = User.objects.filter(username=username).first()

                     # checking if username is already registered
                    if reg_user:
                        return HttpResponse("Username already registered. Try another one!!")
                    else:
                        # saving new user details into database with active status as false
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
                    # message to be displayed to user is render from a html template
                    html_message = render_to_string("accounts/acc_activate_email_template.html",
                                                    context=email_context)
                    to_email_list = [email]
                    # calling the send email function to send verification email and checking if mail is sent successfully
                    if send_email(subject=mail_subject,
                                  html_message=html_message,
                                  to_email=to_email_list):  # to_email must be a tuple of list

                        response = f'A Confirmation email has been sent to {email}.' \
                                   f' Please visit the confirmation link to complete the registration and activate your account.'
                    else:
                        user.delete()
                        response = 'Mail can\'t be send now. Possible Cause - Connection Issue. Try again later sometime.'
                    return HttpResponse(response)
            else:
                # print(registration_form.errors.as_data())
                # in case of invalid form submission returning the error to user
                for e in registration_form.errors:
                    for err in registration_form.errors[e].as_data():
                        return HttpResponse(err)
                return HttpResponse("Form InValid")
    else:
        return HttpResponse("A user is already Logged In.")


# function called when user clicks on the verification link sent through email
def activate(request, uidb64, token,backend='django.contrib.auth.backends.ModelBackend'):
    """
        This function is called when user clicks the activation link sent to his account.
    """
    # extracting user_id from the verification link
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # checking if link is valid and account is not activated before
    if user is not None and account_activation_token.check_token(user, token) and user.is_active == False:
        # activating user account
        user.is_active = True
        user.save()

        # logging in user
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        if user.is_authenticated:
            # redirecting according to account type
            if user.user_type == 'A':
                return redirect('admin_dashboard')
            elif user.user_type == 'P':
                return redirect('provider_dashboard')

            # Asking user for subscribing to some plan
            subscription_plans = SubscriptionPlan.objects.all()
            context = {}
            count = 1

            # returning all the available subscription plans
            for obj in subscription_plans:
                context.update({'plan_' + str(count): (obj.pk, obj.plan_duration, obj.plan_cost)})
                count += 1

            # rendering the response
            return render(request, 'subscribe/templates/subscribe/subscribe.html', {'context': context})

            # return redirect("home_page") # Need to be changed
        else:
            return HttpResponse("Some Error Occured During Login.User Profile was not Created")
    else:
        return HttpResponse("ACTIVATION LINK IS INVALID")


@csrf_exempt
def custom_login(request):

    # extracting form data coming from ajax request
    json_data = json.loads(request.POST.get('data'))
    username = json_data['username']
    password = json_data['password']


    # response to be returned
    context = {
        'is_username_exists': '',
        'is_password_matches': '',
        'is_successful': '',
        'redirect_url': '',
    }

    user = authenticate(username=username, password=password)

    if user is None:
        is_username_exists = User.objects.filter(username=username).first()
        if is_username_exists:
            context['is_password_matches'] = 'Invalid credentials!!'
        else:
            context['is_username_exists'] = 'User does not exists!!'
    else:
        login(request, user)
        context['is_successful'] = 'User logged in successfully!!'

        # redirecting according to account type
        if user.user_type == 'A':
            context['redirect_url'] = 'admin/dashboard'
        elif user.user_type == 'P':
            context['redirect_url'] = 'provider/dashboard'
        elif user.user_type == 'U':
            context['redirect_url'] = ''

    return JsonResponse(context)


def social_redirect_url(request):
    # user = User.objects.filter(username=request.user.username).first()
    # user.user_type = 'U'
    # user.save()
    user_details_exists = UserDetails.objects.filter(user=request.user).first()
    if user_details_exists is None:
        user_details = UserDetails.objects.create(user=request.user, wallet_money=0)
        user_details.save()

    # redirecting according to account type
    if request.user.user_type == 'A':
        return redirect('admin_dashboard')
    elif request.user.user_type == 'P':
        return redirect('provider_dashboard')
    elif request.user.user_type == 'U':
        return redirect('home_page')
