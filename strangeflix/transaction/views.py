from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from accounts.models import CustomUser as User
from accounts.models import UserDetails
from django.contrib.auth.decorators import login_required
from .models import TransactionDetails, TransactionToken, AddMoneyTransactionDetails
from .forms import AddMoneyForm
from datetime import datetime, timedelta
from django.urls import reverse
from django.conf import settings
from django.utils import timezone


@login_required(login_url='home_page')
def wallet_details(request):
    if request.method == 'GET':
        add_money_form = AddMoneyForm()
        user_details = UserDetails.objects.filter(user=request.user).first()
        transactions = TransactionDetails.objects.filter(
            user=request.user,
            payment_type='W'
        ).only('transaction_id', 'transaction_start_time', 'transaction_amount', 'status').union(
            AddMoneyTransactionDetails.objects.filter(
                user=request.user,
            ).only('transaction_id', 'transaction_start_time', 'transaction_amount', 'status')).order_by('-transaction_start_time')
        context = {}
        count = 1
        for obj in transactions:
            context.update({'transaction_' + str(count): (obj.transaction_id, obj.transaction_start_time, obj.transaction_amount*(-1), obj.status)})
            count += 1

        return render(request, 'transaction/wallet.html', {'wallet_bal': user_details.wallet_money, 'add_money_form': add_money_form, 'context': context})
    else:
        raise Http404('Page not found!!')


def insta(email, name, phone, redirect_url, amount):
    response = settings.INSTAMOJO_API.payment_request_create(
        amount=str(amount),
        purpose='Add money to wallet',
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



@login_required(login_url='home_page')
def add_money(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            amount = request.POST.get('amount', 0)

            response = insta(request.user.email,request.user.username,'',request.build_absolute_uri(reverse('add_money_details')),amount)
            amount = int(amount)*(-1)
            transaction_details = AddMoneyTransactionDetails.objects.create(
                transaction_id=response['payment_request']['id'],
                user=request.user,
                transaction_start_time=datetime.now(),
                transaction_amount=amount,
                status=2,
                payment_id=''
            )
            transaction_details.save()
            return redirect(response['payment_request']['longurl'])
        else:
            raise Http404("Page not found!!")
    else:
        return HttpResponse('Invalid Request!! You are not logged in.')



@login_required(login_url='home_page')
def add_money_details(request):
    try:
        payment_status = request.GET['payment_status']
        payment_request_id = request.GET['payment_request_id']
        payment_id = request.GET['payment_id']
    except:
        raise Http404('Page not found')

    transaction_details = AddMoneyTransactionDetails.objects.filter(transaction_id=payment_request_id).first()
    if payment_status == 'Credit':
        transaction_details.status = 5
        transaction_details.payment_id = payment_id
        transaction_details.transaction_start_time = datetime.now(tz=timezone.utc)
        transaction_details.save()

        user_details = UserDetails.objects.filter(user=request.user).first()
        wallet_bal = user_details.wallet_money
        user_details.wallet_money = wallet_bal + transaction_details.transaction_amount*(-1)
        user_details.save()

        return HttpResponse('Hooray!! Your payment is successful. Money added to your wallet!!')
    else:
        transaction_details.status = 1
        transaction_details.transaction_start_time = datetime.now(tz=timezone.utc)
        transaction_details.save()
        raise Http404('Error in processing request. If any amount is deducted from your account it will be refunded in three days.')