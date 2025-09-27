from django.db import models

# Create your models here.
class Category (models.Model):
    categoryName = models.CharField(max_length=100)

    def __str__(self):
        return self.categoryName

class Promo (models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    promoCode = models.CharField(max_length=6, unique=True)
