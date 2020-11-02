# importing django modules
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404 ,JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json

# importing required models
from accounts.models import CustomUser as User
from accounts.models import UserDetails
from .models import TransactionDetails, TransactionToken, AddMoneyTransactionDetails
from home.models import PayPerViewTransaction
from provider.models import SeriesVideos, MovieVideo

# importing required forms
from .forms import AddMoneyForm


# function to get wallet details
@login_required(login_url='home_page')
def wallet_details(request):
    if request.method == 'GET' and request.user.user_type == 'U':

        # add money form
        add_money_form = AddMoneyForm()
        user_details = UserDetails.objects.filter(user=request.user).first()

        # fetching all the wallet transactions made by the user using union from two models
        transactions = TransactionDetails.objects.filter(
            user=request.user,
            payment_type='W'
        ).only('transaction_id', 'transaction_start_time', 'transaction_amount', 'status').union(
            AddMoneyTransactionDetails.objects.filter(
                user=request.user,
            ).only('transaction_id', 'transaction_start_time', 'transaction_amount', 'status')).order_by('-transaction_start_time')

        # fetching user payperview transaction details
        payperview_transactions = PayPerViewTransaction.objects.filter(user_id=request.user)
        payperview_video_ids = PayPerViewTransaction.objects.filter(user_id=request.user).values('video_id').distinct()
        payperview_costs = SeriesVideos.objects.filter(
            video_id__in=payperview_video_ids,
        ).only('video_id__video_id', 'cost_of_video').union(
            MovieVideo.objects.filter(
                video_id__in=payperview_video_ids,
            ).only('video_id__video_id', 'cost_of_video')
        )

        # fetching video details and cost
        video_costs = {}
        for obj in payperview_costs:
            video_costs.update({obj.video_id.video_id: obj.cost_of_video})

        # returning all transactions ordered by date
        all_trans = {}
        for obj in transactions:
            diff = (datetime.now(tz=timezone.utc) - obj.transaction_start_time).total_seconds()
            all_trans.update({diff: (obj.transaction_id, obj.transaction_start_time, obj.transaction_amount*(-1), obj.status)})

        for obj in payperview_transactions:
            diff = (datetime.now(tz=timezone.utc) - obj.transaction_start_time).total_seconds()
            all_trans.update({diff: (obj.transaction_id, obj.transaction_start_time, video_costs[obj.video_id.video_id]*(-1), 5)})

        all_trans = {k: v for k, v in sorted(all_trans.items(), key=lambda item: item[0])}

        context = {}
        count = 1
        # returning all the transactions
        for key in all_trans.keys():
            obj = all_trans[key]
            context.update({'transaction_' + str(count): (obj[0], obj[1], obj[2], obj[3])})
            count += 1

        # returning response
        return render(request, 'transaction/wallet.html', {'wallet_bal': user_details.wallet_money, 'add_money_form': add_money_form, 'context': context})
    else:
        return render(request, 'templates/404.html')


# function to generate a instamojo payment request for adding money to wallet
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


# function to handle add money to wallet request made by the user
@login_required(login_url='home_page')
def add_money(request):
    if request.user.is_authenticated and request.user.user_type == 'U':
        if request.method == 'POST':
            amount = request.POST.get('amount', 0)

            # generating instamojo payment request
            response = insta(request.user.email,request.user.username,'',request.build_absolute_uri(reverse('add_money_details')),amount)
    
            # amounts are saved as negative to have difference between the amount paid and amount added to wallet
            amount = int(amount)*(-1)

            # saving the transaction details
            transaction_details = AddMoneyTransactionDetails.objects.create(
                transaction_id=response['payment_request']['id'],
                user=request.user,
                transaction_start_time=datetime.now(tz=timezone.utc),
                transaction_amount=amount,
                status=2,
                payment_id=''
            )
            transaction_details.save()

            # redirecting to payment gateway
            return redirect(response['payment_request']['longurl'])
        else:
            return render(request, 'templates/404.html')
    else:
        return HttpResponse('Invalid Request!! You are not logged in.')


# function to handle the response send by instamojo on payment completion
@login_required(login_url='home_page')
def add_money_details(request):

    # fetching payment details
    try:
        payment_status = request.GET['payment_status']
        payment_request_id = request.GET['payment_request_id']
        payment_id = request.GET['payment_id']
    except:
        return render(request, 'templates/404.html')

    # fetching transaction details
    transaction_details = AddMoneyTransactionDetails.objects.filter(transaction_id=payment_request_id).first()

    # if transaction amount is paid successfully
    if payment_status == 'Credit':
        # updating the transaction status and saving transaction token
        transaction_details.status = 5
        transaction_details.payment_id = payment_id
        transaction_details.transaction_start_time = datetime.now(tz=timezone.utc)
        transaction_details.save()

        # updating the user wallet balance
        user_details = UserDetails.objects.filter(user=request.user).first()
        wallet_bal = user_details.wallet_money
        user_details.wallet_money = wallet_bal + transaction_details.transaction_amount*(-1)
        user_details.save()

        return HttpResponse('Hooray!! Your payment is successful. Money added to your wallet!!')
    else:
        # updating the transaction status
        transaction_details.status = 1
        transaction_details.payment_id = payment_id
        transaction_details.transaction_start_time = datetime.now(tz=timezone.utc)
        transaction_details.save()

        raise Http404('Error in processing request. If any amount is deducted from your account it will be refunded in three days.')


# function to initiate refund in case the user add money transaction is in pending state but amount credited to website
def initiate_refund_payment(payment_id):
    response = settings.INSTAMOJO_API.refund_create(
        payment_id=payment_id,
        type='TAN',
        body='Refunding amount for completed payment',
        refund_amount=None
    )
    return response


# function to check the payment request payment status
@csrf_exempt
def check_payment_status(request):
    if request.method == 'POST':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        transaction_id = json_data['transaction_id']

        # response object to return as response to ajax request
        context = {
            'is_transaction_exists': '',
            'is_transaction_already_resolved': '',
            'is_user_logged_in': '',
            'if_transaction_belongs_to_user': '',
            'is_successful': '',
            'is_payment_failed': '',
            'is_payment_refunded': '',
        }

        # checking if transaction exists
        transaction_details = AddMoneyTransactionDetails.objects.filter(transaction_id=transaction_id).first()
        if transaction_details is None:
            context['is_transaction_exists'] = 'This transaction does not exists.'
        else:
            # checking is transaction must be in pending stage
            if transaction_details.status != 2:
                context['is_transaction_already_resolved'] = 'This transaction is already resolved.'
            else:
                # checking if user is logged in or not
                if request.user.is_authenticated and request.user.user_type == 'U':
                    if transaction_details.user == request.user:
                        response = settings.INSTAMOJO_API.payment_request_status(transaction_id)
                        # checking if payment is done or not for that payment request id
                        if response['payment_request']['payments'] == []:
                            transaction_details.status = 1
                            transaction_details.save()
                            context['is_payment_failed'] = 'Your transaction failed!!'
                        else:
                            payment_id = ''
                            if 'payment_id' in response['payment_request']['payments'][0].keys():
                                payment_id = response['payment_request']['payments'][0]['payment_id']
                            status = ''
                            if 'status' in response['payment_request']['payments'][0].keys():
                                status = response['payment_request']['payments'][0]['status']

                            # checking if no payment id is there then failed
                            if payment_id == '' or status == '':
                                transaction_details.status = 1
                                transaction_details.save()
                                context['is_payment_failed'] = 'Your transaction failed!!'
                            else:
                                # if money credited than refund the amount
                                if status == 'Credit':
                                    # initiate refund
                                    refund_response = initiate_refund_payment(payment_id)

                                    transaction_details.status = 6
                                    transaction_details.payment_id = payment_id
                                    transaction_details.save()
                                    context['is_payment_refunded'] = 'Payment successfully refunded!!'
                                else:
                                    # else transaction is again failed
                                    transaction_details.status = 1
                                    transaction_details.payment_id = payment_id
                                    transaction_details.save()
                                    context['is_payment_failed'] = 'Your transaction failed!!'
                                context['is_successful'] = 'request processed'
                    else:
                        context['if_transaction_belongs_to_user'] = 'This transaction does not belongs to you.'
                else:
                    context['is_user_logged_in'] = 'You are not logged in.'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')