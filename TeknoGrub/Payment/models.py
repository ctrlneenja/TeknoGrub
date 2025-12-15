from django.db import models
from django.conf import settings


# 1. For Saving Methods in Settings (The Modal)
class UserPaymentMethod(models.Model):
    METHOD_CHOICES = [
        ('GCash', 'GCash'),
        ('Card', 'Credit/Debit Card'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_methods')
    method_type = models.CharField(max_length=20, choices=METHOD_CHOICES)

    # Details
    account_name = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    masked_card_number = models.CharField(max_length=20, blank=True, null=True)
    expiry_date = models.CharField(max_length=5, blank=True, null=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        if self.method_type == 'GCash':
            return f"GCash: {self.account_number}"
        return f"Card: **** {self.masked_card_number}"


# 2. For Transaction Logs (Linked to Orders)
class Payment(models.Model):
    # Use string reference 'Order.Order' to avoid circular import errors
    order = models.ForeignKey('Order.Order', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method_used = models.CharField(max_length=50)  # e.g., "Cash", "GCash"
    transaction_ref = models.CharField(max_length=100, blank=True, null=True)  # e.g. Reference No.
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')  # Paid, Pending, Failed

    def __str__(self):
        return f"Payment #{self.id} - {self.amount}"