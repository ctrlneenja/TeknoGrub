from django.db import models

# Create your models here.
class Cart(models.Model):
    cart = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey("User.Users", on_delete=models.CASCADE, related_name="carts")

class CartItem(models.Model):
    cart_item = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    # menu_item = models.ForeignKey("Menu.MenuItem", on_delete=models.CASCADE, related_name="cart_items")
    # paki check if dapat naa ni kaning ako gi commentan
