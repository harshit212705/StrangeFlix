from django.db import models
from accounts.models import CustomUser as User
# Create your models here.

class RoomControl(models.Model):

    room_id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=100)

    description = models.TextField(max_length=250,default='',blank=True, null=True)

    host_user = models.ForeignKey(User, related_name = 'host_user',on_delete=models.PROTECT)

    members = models.ManyToManyField(User,related_name = 'room_members')

    pending_request = models.ManyToManyField(User,related_name = 'pending_request')

    class Meta:
        verbose_name_plural = "Room Controls"

class UserRoomDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    pending_request = models.ManyToManyField(User,related_name='pending_room_request')

    user_rooms = models.ManyToManyField(RoomControl) 

    class Meta:
        verbose_name_plural = "User Room Details"

