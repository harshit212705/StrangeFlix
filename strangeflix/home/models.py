from django.db import models
from provider.models import Videos
from accounts.models import CustomUser as User


# model for storing transaction details made for pay-per-view service
class PayPerViewTransaction(models.Model):

    transaction_id = models.CharField(max_length=100,blank=True,default='', primary_key=True)

    user_id = models.ForeignKey(User, on_delete=models.PROTECT)

    video_id = models.ForeignKey(Videos, on_delete=models.PROTECT)

    transaction_start_time = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Pay Per View Transaction"

    def __str__(self):
        return str('user--') + str(self.user_id.username) + str(' || video_id--') + str(self.video_id.video_id) + str(' || transaction_time--') + str(self.transaction_start_time)