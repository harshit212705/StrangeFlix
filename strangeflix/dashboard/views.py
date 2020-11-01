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
# Create your views here.


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
        return render(request,'dashboard/user_dashboard.html',context)
    else:
        return render(request, 'templates/404.html')



