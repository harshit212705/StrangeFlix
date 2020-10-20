from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'room/index.html')


def room(request, room_name):
    return render(request, 'room/room.html', {
        'room_name': room_name
    })