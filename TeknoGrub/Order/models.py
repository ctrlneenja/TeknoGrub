from django.db import models

# Create your models here.


class Cart(models.Model):
    cart = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="carts")


class CartItem(models.Model):
    cart_item = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey("canteens.MenuItem", on_delete=models.CASCADE, related_name="cart_items")


class CartItemAddOn(models.Model):
    cart_item_addon = models.AutoField(primary_key=True)
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name="addons")
    addon = models.ForeignKey("canteens.AddOn", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    order = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50)
    order_time = models.DateTimeField(auto_now_add=True)
    pickup_time = models.DateTimeField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    is_reorder = models.BooleanField(default=False)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="orders")
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")


class OrderItem(models.Model):
    order_item = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal_price = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey("canteens.MenuItem", on_delete=models.CASCADE, related_name="order_items")


class OrderItemAddOn(models.Model):
    oder_item_addon = models.AutoField(primary_key=True)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="addons")
    addon = models.ForeignKey("canteens.AddOn", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_ref = models.CharField(max_length=100)
    payment_time = models.DateTimeField(auto_now_add=True)

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    payment_method = models.ForeignKey("users.UserPaymentMethod", on_delete=models.SET_NULL, null=True, blank=True)


class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    login_logs = models.TextField(blank=True, null=True)
    attendance_logs = models.TextField(blank=True, null=True)

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="processed_by")