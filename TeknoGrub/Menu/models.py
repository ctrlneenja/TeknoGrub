from django.db import models
from Canteen.models import Canteen

# Create your models here.

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)

class MenuItem(models.Model):
    menu_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE)
    # MANY-TO-MANY: 
    categories = models.ManyToManyField(
        Category,
        related_name="menu_items"
    )

class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    current_stock = models.IntegerField()
    threshold_level = models.IntegerField()

    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
