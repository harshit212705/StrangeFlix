from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import RoomControl
from accounts.models import CustomUser as User
from subscribe.models import Subscriptions
from datetime import datetime, timedelta, timezone

from django.core import serializers
# Create your views here.
@login_required(login_url='home_page')
def index(request):
    context = {
        'not_subscribed':''
    }
    # checking logged in user subscription plan details
    subscribe = Subscriptions.objects.filter(user=request.user, end_date__gt=datetime.now(tz=timezone.utc)).order_by('-end_date').first()
    if subscribe:
        not_subscribed = False
    else:
        not_subscribed =True
    context['not_subscribed'] = not_subscribed
    return render(request, 'room/index.html',{'context': context})

@login_required
def room(request, room_id):
    room_detail = RoomControl.objects.filter( room_id = room_id).first()
    if room_detail != None:
        if room_detail.host_user == request.user:
            return render(request, 'room/host.html', {
                'room_id': room_id
            })
        elif request.user in room_detail.members.all():
            return render(request, 'room/members.html', {
                'room_id': room_id
            })
        else:
            return render(request, 'templates/404.html')
    else:
        return render(request, 'templates/404.html')

@csrf_exempt
@login_required(login_url='home_page')
def add_new_room(request):
    if request.method =='POST':
        subscribe = Subscriptions.objects.filter(user=request.user, end_date__gt=datetime.now(tz=timezone.utc)).order_by('-end_date').first()
        if subscribe:
            json_data = json.loads(request.POST['data'])
            title = json_data['title']
            description = json_data['description']
            context = {
                'title':title,
                'room_id':'',
                'description': description,
            }
            room = RoomControl.objects.create(
                title=title,
                host_user=request.user,
                description=description,
            )
            room.save()
            context['room_id'] = room.room_id
            return JsonResponse(context)
        else:
            return JsonResponse({})
        


@csrf_exempt
@login_required
def get_host_rooms(request):
    if request.method =='POST':
        subscribe = Subscriptions.objects.filter(user=request.user, end_date__gt=datetime.now(tz=timezone.utc)).order_by('-end_date').first()
        if subscribe:
            user_rooms = RoomControl.objects.filter(host_user = request.user)
            # user_rooms_json = serializers.serialize("json", user_rooms)
            data = []
            for room in user_rooms:
                room_data = {
                    'room_id':room.room_id,
                    'title':room.title,
                    'description':room.description
                }
                data.append(room_data)
            return JsonResponse({'data':data})
        else:
            return JsonResponse({}) 
    else:
        return JsonResponse({})    

def room_details(request,room_id):
    subscribe = Subscriptions.objects.filter(user=request.user, end_date__gt=datetime.now(tz=timezone.utc)).order_by('-end_date').first()
    if subscribe:
        room_detail = RoomControl.objects.filter(host_user = request.user , room_id = room_id).first()
        if(room_detail != None):
            context = {
                'room_id':room_detail.room_id,
                'title':room_detail.title,
                'description':room_detail.description,
            }
            return render(request, 'room/details.html',{'context': context})
        else:
            return render(request, 'templates/404.html')
    else:
        return render(request, 'templates/404.html')

def member_room_details(request,room_id):
    subscribe = Subscriptions.objects.filter(user=request.user, end_date__gt=datetime.now(tz=timezone.utc)).order_by('-end_date').first()
    if subscribe:
        room_detail = RoomControl.objects.filter( room_id = room_id).first()
        if(room_detail != None):
            if request.user in room_detail.members.all():
                context = {
                    'room_id':room_detail.room_id,
                    'title':room_detail.title,
                    'description':room_detail.description,
                    'host':room_detail.host_user.username,
                    'members': [],
                }
                members = []
                for member in room_detail.members.all():
                    members.append(member.username)
                context['members'] = members
                return render(request, 'room/myroomdetails.html',{'context': context})
            else:
                return render(request, 'templates/404.html')
        else:
            return render(request, 'templates/404.html')
    else:
        return render(request, 'templates/404.html')


@csrf_exempt
def get_room_members(request):
    if request.method == 'POST':
        subscribe = Subscriptions.objects.filter(user=request.user, end_date__gt=datetime.now(tz=timezone.utc)).order_by('-end_date').first()
        if subscribe:
            json_data = json.loads(request.POST['data'])
            room_id = json_data['room_id']
            room_detail = RoomControl.objects.filter(host_user = request.user , room_id = room_id).first()
            pending_user  = []
            members = []
            if (room_detail != None):
                for user in room_detail.members.all():
                    members.append(user.username)
                for user in room_detail.pending_request.all():
                    pending_user.append(user.username)
                return JsonResponse({
                    'pending_user':pending_user,
                    'members':members
                })
            else:
                return JsonResponse({})
        else:
            return JsonResponse({})
    else:
        return JsonResponse({})


@csrf_exempt
def send_room_request(request):
    if request.method =='POST':
        json_data = json.loads(request.POST['data'])
        room_id = json_data['room_id']
        username = json_data['username']
        room_detail = RoomControl.objects.filter(host_user = request.user , room_id = room_id).first()
        if (room_detail != None):
            context = {
                'message':''
            }
            new_user = User.objects.filter(username = username).first()

            if new_user == None:
                context['message'] = 'User Not Found'
                return JsonResponse(context)
            subscribe = Subscriptions.objects.filter(user=new_user, end_date__gt=datetime.now(tz=timezone.utc)).order_by('-end_date').first()
            if subscribe == None:
                context['message'] = 'User not subscribed'
                return JsonResponse(context)
            elif request.user  == new_user:
                context['message'] = 'Host cannot be a member'
                return JsonResponse(context)
            elif  new_user in room_detail.members.all():
                context['message'] = 'Person already a member'
                return JsonResponse(context)
            elif new_user in room_detail.pending_request.all():
                context['message'] = 'Request Already Sent'
                return JsonResponse(context)
            else:
                room_detail.pending_request.add(new_user)
                context['message'] = 'Request Sent'
                return JsonResponse(context)
        else:
            return render(request, 'templates/404.html')
    else:
        return render(request, 'templates/404.html')

@csrf_exempt
def get_my_rooms(request):
    if request.method =='POST':
        subscribe = Subscriptions.objects.filter(user=request.user, end_date__gt=datetime.now(tz=timezone.utc)).order_by('-end_date').first()
        if subscribe:
            my_rooms = request.user.room_members.all()
            room_request = request.user.pending_request.all()
            my_rooms_data = []
            room_request_data = []
            for room in my_rooms:
                room_data = {
                    'room_id':room.room_id,
                    'title':room.title,
                    'description':room.description,
                    'host':room.host_user.username
                }
                my_rooms_data.append(room_data)
            for room in room_request:
                room_data = {
                    'room_id':room.room_id,
                    'title':room.title,
                    'description':room.description,
                    'host':room.host_user.username
                }
                room_request_data.append(room_data)
            data = {'my_rooms_data' : my_rooms_data ,'room_request_data' : room_request_data}
            return JsonResponse(data)
        else:
            return JsonResponse({})
    else:
        return JsonResponse({})
    
@csrf_exempt
def accept_room(request):
    if request.method =='POST':
        json_data = json.loads(request.POST['data'])
        room_id = json_data['room_id']
        room_detail = RoomControl.objects.filter(room_id = room_id).first()
        if room_detail != None:
            if request.user in room_detail.pending_request.all():
                room_detail.pending_request.remove(request.user)
                room_detail.members.add(request.user)
                return JsonResponse({'message':'Room Accepted'})
            else:
                return render(request, 'templates/404.html')
        else:
            return render(request, 'templates/404.html')

@csrf_exempt
def reject_room(request):
    if request.method =='POST':
        json_data = json.loads(request.POST['data'])
        room_id = json_data['room_id']
        room_detail = RoomControl.objects.filter(room_id = room_id).first()
        if room_detail != None:
            if request.user in room_detail.pending_request.all():
                room_detail.pending_request.remove(request.user)
                return JsonResponse({'message':'Room Rejected'})
            else:
                return render(request, 'templates/404.html')
        else:
            return render(request, 'templates/404.html')


            
