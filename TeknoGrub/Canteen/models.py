from django.db import models

# Create your models here.
class Canteen(models.Model):
    canteen_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
