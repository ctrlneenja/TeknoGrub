from django.db import models
from Order.models import Order

# Create your models here.
class UserPaymentMethod(models.Model):
    CARD = "CARD"
    GCASH = "GCASH"
    PAYMAYA = "PAYMAYA"

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    payment_method_choices = [
        (CARD, "Credit/Debit Card"),
        (GCASH, "GCash"),
        (PAYMAYA, "PayMaya"),
    ]

    method_type = models.CharField(
        max_length=50,
        choices= payment_method_choices,
        default=CARD  # Optional: set a default choice
    )
    details = models.TextField()

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_ref = models.CharField(max_length=100)
    payment_time = models.DateTimeField(auto_now_add=True)

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    payment_method = models.ForeignKey("users.UserPaymentMethod", on_delete=models.SET_NULL, null=True, blank=True)
