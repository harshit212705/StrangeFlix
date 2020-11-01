from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from accounts.models import CustomUser as User
from accounts.models import UserDetails
from subscribe.models import Subscriptions
from provider.models import Videos,SeriesVideos,MovieVideo,FreeSeriesVideos,FreeMovieVideo,History
from datetime import datetime, timedelta, timezone
from transaction.models import TransactionDetails, TransactionToken, AddMoneyTransactionDetails
from home.models import PayPerViewTransaction



from transaction.forms import AddMoneyForm
# Create your views here.



#To get the Wallet Details
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

        payperview_transactions = PayPerViewTransaction.objects.filter(user_id=request.user)
        payperview_video_ids = PayPerViewTransaction.objects.filter(user_id=request.user).values('video_id').distinct()
        payperview_costs = SeriesVideos.objects.filter(
            video_id__in=payperview_video_ids,
        ).only('video_id__video_id', 'cost_of_video').union(
            MovieVideo.objects.filter(
                video_id__in=payperview_video_ids,
            ).only('video_id__video_id', 'cost_of_video')
        )

        video_costs = {}
        for obj in payperview_costs:
            video_costs.update({obj.video_id.video_id: obj.cost_of_video})

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
        return {'wallet_bal': user_details.wallet_money, 'add_money_form': add_money_form, 'context': context}


@login_required(login_url='home_page')
def user_dashboard(request):
    if request.user.is_authenticated:
        context = {
            'is_subscribed' : '',
            'wallet_balance' : '',
            'end_date':'',
            'favourite_list':'',
        }
        subscribe = Subscriptions.objects.filter(user=request.user, end_date__gt=datetime.now(tz=timezone.utc)).order_by('-end_date').first()
        if subscribe:
            context['end_date'] = subscribe.end_date.strftime("%d %B, %Y, %I:%M %p")
            context['is_subscribed'] = True
        else:
            context['is_subscribed'] = False
        user_details = UserDetails.objects.filter(user=request.user).first()
        context['wallet_balance'] = user_details.wallet_money
        favourite_list = []
        favourites = request.user.favourites.all()
        for favourite in favourites:
            video = ''
            if(favourite.video_id.video_type == 1):
                video_data = FreeSeriesVideos.objects.filter(video_id = favourite.video_id).first()
                if video_data is None:
                    video_data = FreeMovieVideo.objects.filter(video_id = favourite.video_id).first()
                video = video_data
            elif favourite.video_id.video_type == 2:
                video_data = SeriesVideos.objects.filter(video_id = favourite.video_id).first()
                video = video_data
            elif favourite.video_id.video_type == 3:
                video_data = MovieVideo.objects.filter(video_id = favourite.video_id).first()
                video = video_data
            
            favourite_data = {
                'video_id' : favourite.video_id.video_id,
                'video_name' : video.video_name,
                'video_description' : video.video_name,
                'video_image' : video.thumbnail_image.url,

            }
            favourite_list.append(favourite_data)
        context['favourite_list'] = favourite_list

        history_list = []
        histories = History.objects.filter(user_id = request.user).order_by("-timestamp")
        for history in histories:
            video = ''
            if(history.video_id.video_type == 1):
                video_data = FreeSeriesVideos.objects.filter(video_id = history.video_id).first()
                if video_data is None:
                    video_data = FreeMovieVideo.objects.filter(video_id = history.video_id).first()
                video = video_data
            elif history.video_id.video_type == 2:
                video_data = SeriesVideos.objects.filter(video_id = history.video_id).first()
                video = video_data
            elif history.video_id.video_type == 3:
                video_data = MovieVideo.objects.filter(video_id = history.video_id).first()
                video = video_data
            
            history_data = {
                'video_id' : history.video_id.video_id,
                'video_name' : video.video_name,
                'video_description' : video.video_name,
                'video_image' : video.thumbnail_image.url,
                'time' : history.timestamp.strftime("%d %b, %Y, %I:%M %p"),

            }
            history_list.append(history_data)
        context['history_list'] = history_list
        wallet_page_details = wallet_details(request)
        context.update(wallet_page_details)
        return render(request,'dashboard/user_dashboard.html',context)
    else:
        return render(request, 'templates/404.html')



