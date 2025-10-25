from django.db import models

from Canteen.models import Canteen
from Menu.models import MenuItem

from TeknoGrub.Menu.models import Inventory


# Create your models here.
class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100)

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    phone = models.IntegerField()
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    school_id = models.CharField(max_length=20)

class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    canteen_id = models.ForeignKey(Canteen, on_delete=models.CASCADE, related_name='staff')
    login_logs = models.DateTimeField(auto_now_add=True)
    attendance_logs = models.DateTimeField()

class Favorites(models.Model):
    favorite_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    menu_id = models.ForeignKey(Inventory, on_delete=models.CASCADE)

