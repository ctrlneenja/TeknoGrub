from django.db import models
from Cart.models import Cart
#from User.models import Staff

# Create your models here.

class Order(models.Model):
    order = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50)
    order_time = models.DateTimeField(auto_now_add=True)
    pickup_time = models.DateTimeField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    is_reorder = models.BooleanField(default=False)

    user = models.ForeignKey("User.Users", on_delete=models.CASCADE, related_name="orders")
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    staff = models.ForeignKey("User.Staff", on_delete=models.CASCADE)

class OrderItem(models.Model):
    order_item = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal_price = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey("Menu.MenuItem", on_delete=models.CASCADE, related_name="order_items")

class OrderItemAddOn(models.Model):
    oder_item_addon = models.AutoField(primary_key=True)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="addons")
    addon = models.ForeignKey("Menu.AddOn", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)

class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    login_logs = models.TextField(blank=True, null=True)
    attendance_logs = models.TextField(blank=True, null=True)

    #order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="processed_by")