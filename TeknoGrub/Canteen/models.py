from django.db import models

# Create your models here.
class Canteen(models.Model):
    canteen_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)

class MenuItem(models.Model):
    menu_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE)

class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    current_stock = models.IntegerField()
    threshold_level = models.IntegerField()

    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

class AddOn(models.Model):
    add_on_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

class MenuItemAddOn(models.Model):
    menu_item_id = models.AutoField(primary_key=True)
    is_optional = models.BooleanField(null = True)

    menu_id = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    add_on = models.ForeignKey(AddOn, on_delete=models.CASCADE)

class MenuItemCategories(models.Model):
    menu_item_category_id = models.AutoField(primary_key=True)

    menu_id = models.ForeignKey(MenuItem, on_delete=models.CASCADE)