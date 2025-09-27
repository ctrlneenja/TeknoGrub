from django.db import models
from Order.models import Order

# Create your models here.
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_ref = models.CharField(max_length=100)
    payment_time = models.DateTimeField(auto_now_add=True)

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    payment_method = models.ForeignKey("users.UserPaymentMethod", on_delete=models.SET_NULL, null=True, blank=True)
