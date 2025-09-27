from django.db import models

from TeknoGrub.User.models import Users
# Create your models here.
class Notifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user')
    message = models.CharField(max_length=500)
    type = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)