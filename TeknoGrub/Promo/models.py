from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class PromoName(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20)  # e.g., percentage, fixed
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    per_user_limit = models.IntegerField(default=1)
    max_uses = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.code})"


class PromoRedemption(models.Model):
    redeemed_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("User.Users", on_delete=models.CASCADE, related_name="redeemed_promos")
    promo = models.ForeignKey(PromoName, on_delete=models.CASCADE, related_name="redemptions")
