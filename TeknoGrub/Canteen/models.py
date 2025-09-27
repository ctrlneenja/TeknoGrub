from django.db import models

from TeknoGrub import User
from TeknoGrub.Order.models import Order
from TeknoGrub.User.models import User


# Create your models here.
class Canteen(models.Model):
    canteen_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)

class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    log_in_logs = models.DateTimeField(auto_now_add=True)
    attendance_logs = models.DateTimeField(auto_now_add=True)

    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    canteen_id = models.ForeignKey(Canteen, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
