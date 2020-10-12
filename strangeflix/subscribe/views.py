# importing django modules
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.urls import reverse
from django.conf import settings
import hashlib

# importing required models
from .models import SubscriptionPlan
from accounts.models import UserDetails, CustomUser
from accounts.models import CustomUser as User
from .models import SubscriptionPlan, Subscriptions, SubscriptionAdditionalTransaction
from transaction.models import TransactionDetails, TransactionToken


# function to render all the available subscription plans to user
@login_required(login_url='home_page')
def subscription_plans(request):
    if request.method == 'GET':
        subscription_plans = SubscriptionPlan.objects.all()
        context = {}
        count = 1
        for obj in subscription_plans:
            context.update({'plan_' + str(count): (obj.pk, obj.plan_duration, obj.plan_cost)})
            count += 1

        # returning response
        return render(request, 'subscribe/subscribe.html', {'context': context})
    else:
        return render(request, 'templates/404.html')


# function to be called when user wishes to purchase a subcsription plan
@login_required(login_url='home_page')
def subscribe_plan(request,plan_id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            # fetching the plan details
            plan = SubscriptionPlan.objects.filter(pk=plan_id).first()
            if plan:
                user_details = UserDetails.objects.filter(user=request.user).first()
                context = {
                    'user_id': request.user.pk,
                    'plan_id': plan.pk,
                    'plan_duration': plan.plan_duration,
                    'wallet_money': user_details.wallet_money,
                    'plan_cost': plan.plan_cost,
                }
                return render(request, 'subscribe/payment_details.html', context)
            else:
                return render(request, 'templates/404.html')
        else:
            return render(request, 'templates/404.html')
    else:
        return HttpResponse('Invalid Request!! You are not logged in.')


# function to be called using ajax when user wishes to use his wallet money for transaction
def use_wallet_bal(request):
    # extracting user and plan details
    user_id = request.GET.get('user_id', None)
    plan_id = request.GET.get('plan_id', None)
    user = User.objects.filter(pk=user_id).first()
    plan = SubscriptionPlan.objects.filter(pk=plan_id).first()

    # response object to be returned
    context = {
        'is_user_exists': 'No',
        'is_plan_exists': 'No',
        'remaining_amount': 0,
    }

    # checking if user exists
    if user:
        context['is_user_exists'] = 'Yes'
        wallet_bal = UserDetails.objects.filter(user=user).first().wallet_money

        # checking if the plan exists which user wants to purchase
        if plan:
            context['is_plan_exists'] = 'Yes'
            plan_cost = plan.plan_cost

            # checking if plan cost is more than the money user have in his wallet
            if plan_cost > wallet_bal:
                context['remaining_amount'] = plan_cost - int(wallet_bal)

    return JsonResponse(context)


# function to generate an instamojo payment request to pay for purchasing subscription
def insta(email, name, phone, redirect_url, amount):
    response = settings.INSTAMOJO_API.payment_request_create(
        amount=str(amount),
        purpose='Purchasing Subscription',
        buyer_name=name,
        send_email=True,
        email=email,
        phone=phone,
        redirect_url=redirect_url,
        allow_repeated_payments=False,
        #webhook=webhook, impp - webhook function must be csrf_exempt as instamojo server
        # sends a post request to our server but without csrf token
    )
    return response

# function to initiate refund in case the card transaction is completed but now the user doesnot have enough balance in his wallet
def initiate_refund(payment_id):
    response = settings.INSTAMOJO_API.refund_create(
        payment_id=payment_id,
        type='TAN',
        body='Lack of funds in wallet',
        refund_amount=None
    )
    return response


# function to handle the payment request made by the user
@csrf_exempt
@login_required(login_url='home_page')
def make_payment(request, plan_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # checking if user wants to use his wallet balance or not
            is_checked = request.POST.get('checkbox', None)
            # fetching user details
            user_details = UserDetails.objects.filter(user=request.user).first()
            wallet_bal = user_details.wallet_money
            # fetching plan details
            plan = SubscriptionPlan.objects.filter(pk=plan_id).first()
            plan_cost = plan.plan_cost
            amt_to_be_charged = plan_cost

            # If user wants to use the wallet balance
            if is_checked:
                # If user has sufficient balance in his/her account
                if wallet_bal >= plan_cost:
                    # generating a unique transaction id for wallet payment
                    transaction_id = str(request.user.id) + str(datetime.now())
                    hash_object = hashlib.sha1(transaction_id.encode('utf-8'))
                    hex_dig = hash_object.hexdigest()

                    # saving wallet transaction to database
                    transaction_details = TransactionDetails.objects.create(
                        transaction_id=hex_dig,
                        user=request.user,
                        sub_plan_id=plan,
                        transaction_start_time=datetime.now(),
                        payment_type='W',
                        transaction_amount=plan_cost,
                        status=5
                    )
                    transaction_details.save()

                    # adding details of the subscription purchased by the user
                    no_of_days = 30*plan.plan_duration
                    end_date = datetime.now() + timedelta(days=no_of_days)
                    subscription = Subscriptions.objects.create(
                        user=request.user,
                        sub_plan_id=plan,
                        end_date=end_date,
                        transaction_id=transaction_details
                    )
                    subscription.save()

                    # updating user wallet balance
                    user_details.wallet_money = wallet_bal - plan_cost
                    user_details.save()
                    return HttpResponse('Hooray!! Your payment is successful. Enjoy streaming!!')
                else:
                    amt_to_be_charged = plan_cost - wallet_bal
            else:
                amt_to_be_charged = plan_cost

            # generating a instamojo payment request for the remaining amount to be paid by the user
            response = insta(request.user.email,request.user.username,'',request.build_absolute_uri(reverse('payment_details')),amt_to_be_charged)
            # print(response)

            # adding transaction details for card payment oto database with status as pending
            transaction_details = TransactionDetails.objects.create(
                transaction_id=response['payment_request']['id'],
                user=request.user,
                sub_plan_id=plan,
                transaction_start_time=datetime.now(),
                payment_type='C',
                transaction_amount=amt_to_be_charged,
                status=2
            )
            transaction_details.save()

            # redirecting user to payment gateway
            return redirect(response['payment_request']['longurl'])
        else:
            return render(request, 'templates/404.html')
    else:
        return HttpResponse('Invalid Request!! You are not logged in.')


# function to handle the response given by instamojo after completion of payment
@login_required(login_url='home_page')
def payment_details(request):
    # fetching the payment details
    try:
        payment_status = request.GET['payment_status']
        payment_request_id = request.GET['payment_request_id']
        payment_id = request.GET['payment_id']
    except:
        return render(request, 'templates/404.html')

    # fetching the transaction details and updating status to completed
    transaction_details = TransactionDetails.objects.filter(transaction_id=payment_request_id).first()
    transaction_details.status = 4
    transaction_details.save()

    # checking if payment is done successfully and amount is credited
    if payment_status == 'Credit':
        # fetching plan details
        plan = transaction_details.sub_plan_id
        plan_cost = plan.plan_cost
        amount_paid = transaction_details.transaction_amount

        # If user paid the whole plan cost using card
        if amount_paid == plan_cost:
            # saving the payment id or transaction token to database
            transaction_token = TransactionToken.objects.create(
                transaction_id=transaction_details,
                payment_id=payment_id,
                transaction_end_time=datetime.now(),
                status=2
            )
            transaction_token.save()

            # adding details of the subscription purchased by the user
            no_of_days = 30*(plan.plan_duration)
            end_date = datetime.now() + timedelta(days=no_of_days)
            subscription = Subscriptions.objects.create(
                user=request.user,
                sub_plan_id=plan,
                end_date=end_date,
                transaction_id=transaction_details
            )
            subscription.save()
            return HttpResponse('Hooray!! Your payment is successful. Enjoy streaming!!')
        else:
            # how much amount to be deducted from wallet
            wallet_bal_to_be_deducted = plan_cost - amount_paid
            # fetching user details
            user_details = UserDetails.objects.filter(user=request.user).first()
            wallet_bal = user_details.wallet_money

            # If user has sufficient balance in his/her wallet that he/she asked to deduct
            if wallet_bal >= wallet_bal_to_be_deducted:
                # saving the payment id or transaction token to database
                transaction_token = TransactionToken.objects.create(
                    transaction_id=transaction_details,
                    payment_id=payment_id,
                    transaction_end_time=datetime.now(),
                    status=2
                )
                transaction_token.save()

                # generating a unique transaction id for wallet payment
                transaction_id = str(request.user.id) + str(datetime.now())
                hash_object = hashlib.sha1(transaction_id.encode('utf-8'))
                hex_dig = hash_object.hexdigest()

                # saving wallet transaction to database
                trans_details = TransactionDetails.objects.create(
                    transaction_id=hex_dig,
                    user=request.user,
                    sub_plan_id=plan,
                    transaction_start_time=datetime.now(),
                    payment_type='W',
                    transaction_amount=wallet_bal_to_be_deducted,
                    status=5
                )
                trans_details.save()

                # adding details of the subscription purchased by the user
                no_of_days = 30*plan.plan_duration
                end_date = datetime.now() + timedelta(days=no_of_days)
                subscription = Subscriptions.objects.create(
                    user=request.user,
                    sub_plan_id=plan,
                    end_date=end_date,
                    transaction_id=transaction_details
                )
                subscription.save()

                 # updating user wallet balance
                user_details.wallet_money = wallet_bal - wallet_bal_to_be_deducted
                user_details.save()

                # saving additional transaction id corresponding to subscription because payment is made using two methods
                subscription_additional_transaction = SubscriptionAdditionalTransaction.objects.create(
                    subscription_id=subscription,
                    transaction_id=trans_details
                )
                subscription_additional_transaction.save()
                return HttpResponse('Hooray!! Your payment is successful. Enjoy streaming!!')
            else:
                # if user wallet has insufficient balance
                # initiating a refund for user transaction
                refund_response = initiate_refund(payment_id)
                # print(refund_response)

                # saving the payment id or transaction token to database
                transaction_token = TransactionToken.objects.create(
                    transaction_id=transaction_details,
                    payment_id=payment_id,
                    transaction_end_time=datetime.now(),
                    status=3
                )
                transaction_token.save()

                # generating a unique transaction id for wallet payment
                transaction_id = str(request.user.id) + str(datetime.now())
                hash_object = hashlib.sha1(transaction_id.encode('utf-8'))
                hex_dig = hash_object.hexdigest()

                # saving wallet transaction to database
                trans_details = TransactionDetails.objects.create(
                    transaction_id=hex_dig,
                    user=request.user,
                    sub_plan_id=plan,
                    transaction_start_time=datetime.now(),
                    payment_type='W',
                    transaction_amount=wallet_bal_to_be_deducted,
                    status=1
                )
                trans_details.save()
                raise Http404('It seems your wallet do not have the required balance. Your subscription required has failed and any deductions from your account will be refunded back in three days.')
    else:
        # if card payment is failed and money is not credited
        # saving the payment id or transaction token to database
        transaction_token = TransactionToken.objects.create(
            transaction_id=transaction_details,
            payment_id=payment_id,
            transaction_end_time=datetime.now(),
            status=1
        )
        transaction_token.save()
        raise Http404('Error in processing request. If any amount is deducted from your account it will be refunded in three days.')